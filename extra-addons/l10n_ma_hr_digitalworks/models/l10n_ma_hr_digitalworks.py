# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing det


from odoo import fields, models, api
from odoo.addons import decimal_precision as dp
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


class hr_contract(models.Model):
    _inherit = 'hr.contract'

    salaire_base = fields.Float(u'Salaire Base')
    indimnite_panier = fields.Float(u'Indimnité Panier')
    indimnite_transport = fields.Float(u'Indimnité Transport')
    grade_id = fields.Many2one('hr.employee.dw.grade', string="Employé Grade")
    category_id = fields.Many2one('hr.employee.dw.category', string="Employé Categorie")

    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        """ This function sets partner email address based on partner
        """
        self.wage = self.grade_id.salaire_net
        self.salaire_base = self.grade_id.salaire_base
        self.indimnite_panier = self.grade_id.indimnite_panier
        self.indimnite_transport = self.grade_id.indimnite_transport

    @api.onchange('category_id','type_id','trial_date_start')
    def _onchange_category_id(self):
        """ This function sets partner email address based on partner
        """
        if self.trial_date_start:
            if (self.type_id.name == "CDI" and self.category_id.name=="Employee"):
                self.trial_date_end = (datetime.strptime(self.trial_date_start,'%Y-%m-%d') + relativedelta(months=6)).strftime('%Y-%m-%d')
            elif (self.type_id.name == "CDI" and self.category_id.name=="Cadre"):
                self.trial_date_end = (datetime.strptime(self.trial_date_start,'%Y-%m-%d') + relativedelta(months=3)).strftime('%Y-%m-%d')

class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    indimnite_pro = fields.Float(u'Heures Production')
    indimnite_pro_tx_normal = fields.Float(compute='_compute_indimnite_pro_tx_normal',
                                           string=u'Heures Production (Taux Normal)')
    indimnite_formation = fields.Float(u'Heures Formation')
    indimnite_conge = fields.Float(u'Heures Conge')
    bonus = fields.Float('Bonus')

    base_calcul_pack = fields.Float(compute='_compute_base_calcul_pack', string=u'Base Pack HS')
    pack_taux = fields.Float(compute='_compute_pack_taux', string=u'Taux Pack HS')

    base_calcul_challenge = fields.Float(compute='_compute_base_calcul_challenge', string=u'Base Challenge')
    challenge = fields.Float(compute='_compute_challenge', string=u'Challenge')

    retenu_sur_salaire = fields.Float(u'Retenu sur Salaire')
    reguls = fields.Float(u'Réguls')

    def _compute_indimnite_pro(self):
        timesheets_cms_object = self.env['hr.timesheet.cms']
        timesheets_cms_hours = timesheets_cms_object.search([('employee_id', '=', self.employee_id.id),
                                                                ('date', '>=', self.date_from),
                                                                ('date', '<=', self.date_to) ])
        total_hours = 0.0
        for timesheet_cms_hours in timesheets_cms_hours:
            total_hours += timesheet_cms_hours.temps_paie_cms

        self.indimnite_pro = total_hours

    @api.depends('indimnite_pro')
    def _compute_indimnite_pro_tx_normal(self):
        for record in self:
            if (record.indimnite_pro <= 191):
                self.indimnite_pro_tx_normal = self.indimnite_pro
            if (record.indimnite_pro > 191):
                self.indimnite_pro_tx_normal = 191


    @api.depends('indimnite_pro', 'indimnite_conge')
    def _compute_base_calcul_pack(self):
        """ This function sets partner email address based on partner
        """
        for record in self:
            if (record.indimnite_pro + record.indimnite_conge - 191 >= 0):
                record.base_calcul_pack = record.indimnite_pro + record.indimnite_conge - 191
            else:
                record.base_calcul_pack = 0

    @api.depends('indimnite_pro', 'indimnite_conge')
    def _compute_base_calcul_pack(self):
        """ This function sets partner email address based on partner
        """
        for record in self:
            if (record.indimnite_pro + record.indimnite_conge - 191 >= 0):
                record.base_calcul_pack = record.indimnite_pro + record.indimnite_conge - 191
            else:
                record.base_calcul_pack = 0

    @api.depends('base_calcul_pack')
    def _compute_pack_taux(self):
        for record in self:
            if (record.base_calcul_pack <= 0):
                record.pack_taux = 0
            elif (record.base_calcul_pack <= 10 and record.base_calcul_pack > 0):
                record.pack_taux = 1.25
            elif (record.base_calcul_pack <= 20 and record.base_calcul_pack > 10):
                record.pack_taux = 1.5
            elif (record.base_calcul_pack <= 30 and record.base_calcul_pack > 20):
                record.pack_taux = 1.75
            elif (record.base_calcul_pack > 30):
                record.pack_taux = 2.0

    @api.depends('indimnite_pro', 'indimnite_conge')
    def _compute_base_calcul_challenge(self):
        for record in self:
            record.base_calcul_challenge = record.indimnite_pro + record.indimnite_conge

    @api.depends('base_calcul_challenge')
    def _compute_challenge(self):
        if (self.base_calcul_challenge <= 191):
            self.challenge = 0.0
        elif (self.base_calcul_challenge > 191):
            self.challenge = 500


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    matricule_dw = fields.Char(u'Matricule DW',copy=False)
    matricule_dw_bcp = fields.Char(u'Matricule DW BCP',copy=False)
    adresse_personnelle = fields.Char(string="Adresse Personnelle", required=False)
    ville_personnelle = fields.Char(string="Ville", required=False)
    num_carte_sejour = fields.Char(u'N° Carte Séjour')
    date_expiration_cin = fields.Date('Date Expiration CIN')
    date_expiration_passport = fields.Date('Date Expiration Passport')
    date_expiration_carte_sejour = fields.Date('Date Expiration Carte Sejour')

    ##### CHECK LIST ####
    ##### Documents Apportés ####
    #####  => Employé ####

    has_cin = fields.Boolean(u'Check CIN', default=False)
    has_carte_sejour = fields.Boolean(u'Check Carte Séjour', default=False)
    has_photos = fields.Boolean(u'Check Photos', default=False)
    has_passport = fields.Boolean(u'Check Passport', default=False)
    has_fiche_anthropometrique = fields.Boolean(u'Check Fiche Anthropométrique', default=False)
    has_radio_pulmonaire = fields.Boolean(u'Check Radio Pulmonaire', default=False)
    has_justif_salaire = fields.Boolean(u'Check Justif Salaire', default=False)
    has_rib = fields.Boolean(u'Check RIB', default=False)
    has_stc = fields.Boolean(u'Check STC', default=False)
    has_cnss = fields.Boolean(u'Check CNSS', default=False)
    has_attestation_travail = fields.Boolean(u'Check Attestation Travail', default=False)
    has_diplome = fields.Boolean(u'Check Diplome(s)', default=False)

    date_depot_cin = fields.Datetime(u'Date Dépôt CIN')
    date_depot_carte_sejour = fields.Datetime(u'Date Dépôt Carte séjour')
    date_depot_photos = fields.Datetime(u'Date Dépôt Photos')
    date_depot_passport = fields.Datetime(u'Date Dépôt Passport')
    date_depot_fiche_anthropometrique = fields.Datetime(u'Date Dépôt Fiche Anthropométrique')
    date_depot_radio_pulmonaire = fields.Datetime(u'Date Dépôt Radio Pulmonaire')
    date_depot_justif_salaire = fields.Datetime(u'Date Dépôt Justif Salaire')
    date_depot_attestation_travail = fields.Datetime(u'Date Dépôt Attestation Travail')
    date_depot_diplome = fields.Datetime(u'Date Dépôt Diplôme(s)')
    date_depot_rib = fields.Datetime(u'Date Dépôt RIB')
    date_depot_stc = fields.Datetime(u'Date Dépôt STC')
    date_depot_cnss = fields.Datetime(u'Date Dépôt CNSS')

    #####  => Conjoint ####
    has_conjoint_actmariage = fields.Boolean(u'Check Acte Marriage', default=False)
    has_conjoint_cin = fields.Boolean(u'Check CIN', default=False)
    has_conjoint_attestation_travail = fields.Boolean(u'Check Attestation Travail', default=False)
    has_cojoint_cnss = fields.Boolean(u'Check CNSS', default=False)

    date_depot_conjoint_actmariage = fields.Datetime(u'Date Dépôt Acte Marriage')
    date_depot_conjoint_cin = fields.Datetime(u'Date Dépôt CIN')
    date_depot_conjoint_attestation_travail = fields.Datetime(u'Date Dépôt Attestation Travail')
    date_depot_cojoint_cnss = fields.Datetime(u'Date Dépôt CNSS')

    #####  => Enfants ####
    has_enfant_actnaissance = fields.Boolean(u'Check Acte Naissance', default=False)
    has_enfant_cert_vie = fields.Boolean(u'Check Certif Vie Collectif', default=False)
    has_enfant_cert_scol = fields.Boolean(u'Check Certif Scolarité', default=False)
    has_enfant_cert_alloc = fields.Boolean(u'Check Certif Allocation Familiale / Mutuelle', default=False)

    date_depot_enfant_actnaissance = fields.Datetime(u'Date Dépôt Acte Naissance')
    date_depot_enfant_cert_vie = fields.Datetime(u'Date Certif Vie Collectif')
    date_depot_enfant_cert_scol = fields.Datetime(u'Date Dépôt Certif Scolarité')
    date_depot_enfant_cert_alloc = fields.Datetime(u'Date Dépôt Certif Allocation')

    ##### Suivi administratif Collaborateur ####
    ##### Contrat de travail #####
    contract_remis_pr_sign = fields.Boolean('Contrat remis pour signature', default=False)
    contract_recu_sign_leg = fields.Boolean(u'Contrat reçu signé et légalisé', default=False)
    contract_en_cours_sign = fields.Boolean('Contrat en cours de signature', default=False)
    contract_remis_sign = fields.Boolean(u'Contrat signé remis', default=False)

    date_contract_remis_pr_sign = fields.Datetime('Date de remise du contrat')
    date_contract_recu_sign_leg = fields.Datetime('Date de reception du contrat')
    date_contract_en_cours_sign = fields.Datetime('Date de signature')
    date_contract_remis_sign = fields.Datetime(u'Date de remise du contrat signé')

    #### Charte ####

    rgl_remis_au_col = fields.Boolean(u'Règlement intérieur remis', default=False)
    faute_grave = fields.Boolean(u'Fautes graves remises', default=False)
    charte_info_remis = fields.Boolean('charte informatique remise', default=False)
    regl_recu_sign = fields.Boolean(u'Règlement intérieur reçu signé', default=False)
    faute_grave_recu_sign = fields.Boolean(u'Fautes graves reçues signées', default=False)
    charte_info_recu_sign = fields.Boolean(u'charte informatique reçue signée', default=False)

    date_rgl_remis_au_col = fields.Datetime(u'Date de remise du réglement intérieur')
    date_faute_grave = fields.Datetime('Date de remise des fautes graves')
    date_charte_info_remis = fields.Datetime('Date de remise de la charte informatique')
    date_regl_recu_sign = fields.Datetime(u'Date de signature du réglement intérieur')
    date_faute_grave_recu_sign = fields.Datetime(u'Date de signature fautes graves')
    date_charte_info_recu_sign = fields.Datetime(u'Date de signature de la charte informatique')

    ##### CNSS & SAHAM ####
    ##### CNSS #####

    form_remis_pr_sign = fields.Boolean('Formulaire remis pour signature', default=False)
    form_transmis_cnss = fields.Boolean(u'Formulaire transmis à la CNSS', default=False)
    carte_recu = fields.Boolean(u'Carte reçue', default=False)
    carte_remise = fields.Boolean('Carte remise au collaborateur', default=False)

    date_form_remis = fields.Datetime('Date de remise')
    date_form_transmis = fields.Datetime(u'Date de transmission à la CNSS')
    date_carte_recu = fields.Datetime('Date de reception de la carte')
    date_carte_remise= fields.Datetime('Date de remise de la carte')

    ##### SAHAM #####

    bds_remis = fields.Boolean('BDS remis au collaborateur', default=False)
    bds_recu = fields.Boolean(u'BDS reçu par le collborateur', default=False)
    bds_transmis_saham = fields.Boolean(u'BDS Transmis à SAHAM', default=False)
    photo_transmis_securt = fields.Boolean(u'Photo transmise à la sécurité', default=False)

    date_bds_remis = fields.Datetime('Date de remise de BDS')
    date_bds_recu = fields.Datetime('Date de reception de BDS')
    date_bds_transmis_saham = fields.Datetime(u'Date de transmission de BDS à SAHAM')
    date_photo_transmis_securt = fields.Datetime(u'Date de transmission de la photo à la sécurité')

    _sql_constraints = [
        ('matricule_dw', 'unique(matricule_dw)',
         'The Employee DW Matricule must be unique across the company(s).'),
    ]

    ######################################################
    #### on_change method for document admin checkbox ####
    ######################################################
    @api.onchange('has_cin')
    def _onchange_has_cin(self):
        if (self.has_cin):
            self.date_depot_cin = fields.Datetime.now()
        else:
            self.date_depot_cin = False

    @api.onchange('has_diplome')
    def _onchange_has_diplome(self):
        if (self.has_diplome):
            self.date_depot_diplome = fields.Datetime.now()
        else:
            self.date_depot_diplome = False

    @api.onchange('has_carte_sejour')
    def _onchange_has_carte_sejour(self):
        if (self.has_carte_sejour):
            self.date_depot_carte_sejour = fields.Datetime.now()
        else:
            self.date_depot_carte_sejour = False

    @api.onchange('has_photos')
    def _onchange_has_photos(self):
        if (self.has_photos):
            self.date_depot_photos = fields.Datetime.now()
        else:
            self.date_depot_photos = False

    @api.onchange('has_passport')
    def _onchange_has_passport(self):
        if (self.has_passport):
            self.date_depot_passport = fields.Datetime.now()
        else:
            self.date_depot_passport = False

    @api.onchange('has_fiche_anthropometrique')
    def _onchange_has_fiche_anthropometrique(self):
        if (self.has_fiche_anthropometrique):
            self.date_depot_fiche_anthropometrique = fields.Datetime.now()
        else:
            self.date_depot_fiche_anthropometrique = False

    @api.onchange('has_radio_pulmonaire')
    def _onchange_has_radio_pulmonaire(self):
        if (self.has_radio_pulmonaire):
            self.date_depot_radio_pulmonaire = fields.Datetime.now()
        else:
            self.date_depot_radio_pulmonaire = False

    @api.onchange('has_justif_salaire')
    def _onchange_has_justif_salaire(self):
        if (self.has_justif_salaire):
            self.date_depot_justif_salaire = fields.Datetime.now()
        else:
            self.date_depot_justif_salaire = False

    @api.onchange('has_rib')
    def _onchange_has_rib(self):
        if (self.has_rib):
            self.date_depot_rib = fields.Datetime.now()
        else:
            self.date_depot_rib = False

    @api.onchange('has_stc')
    def _onchange_has_stc(self):
        if (self.has_stc):
            self.date_depot_stc = fields.Datetime.now()
        else:
            self.date_depot_stc = False

    @api.onchange('has_cnss')
    def _onchange_has_cnss(self):
        if (self.has_cnss):
            self.date_depot_cnss = fields.Datetime.now()
        else:
            self.date_depot_cnss = False

    @api.onchange('has_attestation_travail')
    def _onchange_has_attestation_travail(self):
        if (self.has_attestation_travail):
            self.date_depot_attestation_travail = fields.Datetime.now()
        else:
            self.date_depot_attestation_travail = False
    ###############################################
    #### on_change method for Contrat checkbox ####
    ###############################################
    @api.onchange('contract_remis_pr_sign')
    def _onchange_contract_remis_pr_sign(self):
        if (self.contract_remis_pr_sign):
            self.date_contract_remis_pr_sign = fields.Datetime.now()
        else:
            self.date_contract_remis_pr_sign = False

    @api.onchange('contract_recu_sign_leg')
    def _onchange_contract_recu_sign_leg(self):
        if (self.contract_recu_sign_leg):
            self.date_contract_recu_sign_leg = fields.Datetime.now()
        else:
            self.date_contract_recu_sign_leg = False

    @api.onchange('contract_en_cours_sign')
    def _onchange_contract_en_cours_sign(self):
        if (self.contract_en_cours_sign):
            self.date_contract_en_cours_sign = fields.Datetime.now()
        else:
            self.date_contract_en_cours_sign = False

    @api.onchange('contract_remis_sign')
    def _onchange_contract_remis_sign(self):
        if (self.contract_remis_sign):
            self.date_contract_remis_sign = fields.Datetime.now()
        else:
            self.date_contract_remis_sign = False

    ############################################
    #### on_change method for CHARTE checkbox ####
    ############################################
    @api.onchange('rgl_remis_au_col')
    def _onchange_rgl_remis_au_col(self):
        if (self.rgl_remis_au_col):
            self.date_rgl_remis_au_col = fields.Datetime.now()
        else:
            self.date_rgl_remis_au_col = False

    @api.onchange('faute_grave')
    def _onchange_faute_grave(self):
        if (self.faute_grave):
            self.date_faute_grave = fields.Datetime.now()
        else:
            self.date_faute_grave = False

    @api.onchange('charte_info_remis')
    def _onchange_charte_info_remis(self):
        if (self.charte_info_remis):
            self.date_charte_info_remis = fields.Datetime.now()
        else:
            self.date_charte_info_remis = False

    @api.onchange('regl_recu_sign')
    def _onchange_regl_recu_sign(self):
        if (self.regl_recu_sign):
            self.date_regl_recu_sign = fields.Datetime.now()
        else:
            self.date_regl_recu_sign = False

    @api.onchange('faute_grave_recu_sign')
    def _onchange_faute_grave_recu_sign(self):
        if (self.faute_grave_recu_sign):
            self.date_faute_grave_recu_sign = fields.Datetime.now()
        else:
            self.date_faute_grave_recu_sign = False

    @api.onchange('charte_info_recu_sign')
    def _onchange_charte_info_recu_sign(self):
        if (self.charte_info_recu_sign):
            self.date_charte_info_recu_sign = fields.Datetime.now()
        else:
            self.date_charte_info_recu_sign = False
    ############################################
    #### on_change method for SAHAM checkbox ####
    ############################################
    @api.onchange('bds_remis')
    def _onchange_bds_remis(self):
        if (self.bds_remis):
            self.date_bds_remis = fields.Datetime.now()
        else:
            self.date_bds_remis = False

    @api.onchange('bds_recu')
    def _onchange_bds_recu(self):
        if (self.bds_recu):
            self.date_bds_recu = fields.Datetime.now()
        else:
            self.date_bds_recu = False

    @api.onchange('bds_transmis_saham')
    def _onchange_bds_transmis_saham(self):
        if (self.bds_transmis_saham):
            self.date_bds_transmis_saham = fields.Datetime.now()
        else:
            self.date_bds_transmis_saham = False
    @api.onchange( 'photo_transmis_securt')
    def _onchange_photo_transmis_securt(self):
        if (self.photo_transmis_securt):
            self.date_photo_transmis_securt = fields.Datetime.now()
        else:
            self.date_photo_transmis_securt = False
    ############################################
    #### on_change method for cnss checkbox ####
    ############################################
    @api.onchange('form_remis_pr_sign')
    def _onchange_form_remis_pr_sign(self):
        if (self.form_remis_pr_sign):
            self.date_form_remis = fields.Datetime.now()
        else:
            self.date_form_remis = False

    @api.onchange( 'form_transmis_cnss')
    def _onchange_form_transmis_cnss(self):
        if (self.form_transmis_cnss):
            self.date_form_transmis = fields.Datetime.now()
        else:
            self.date_form_transmis = False

    @api.onchange('carte_recu')
    def _onchange_carte_recu(self):
        if (self.carte_recu):
            self.date_carte_recu = fields.Datetime.now()
        else:
            self.date_carte_recu = False

    @api.onchange('carte_remise')
    def _onchange_carte_remise(self):
        if (self.carte_remise):
            self.date_carte_remise = fields.Datetime.now()
        else:
            self.date_carte_remise = False

class EmployeeDWGrde(models.Model):
    _name = "hr.employee.dw.grade"
    _description = "Employee DW Grade"

    name = fields.Char(string="Grade", required=True)
    salaire_base = fields.Float(u'Salaire de base')
    salaire_net = fields.Float(u'Salaire Net')
    indimnite_transport = fields.Float(u'Indimnité Transport')
    indimnite_panier = fields.Float(u'Indimnité Panier')

    @api.onchange('indimnite_panier', 'indimnite_transport', 'salaire_base')
    def _onchange_indimnite_salaire(self):
        """ This function compute salaire net"""
        self.salaire_net = self.salaire_base + self.indimnite_panier + self.indimnite_transport

class EmployeeDWCategory(models.Model):
    _name = "hr.employee.dw.category"
    _description = "Employee DW Category"

    name = fields.Char(string="Catégorie Employé", required=True)

class HrTimesheetCMS(models.Model):
    _name = "hr.timesheet.cms"
    _description = "HR Timesheet CMS"

    date = fields.Date('Date',required=True)
    employee_id = fields.Many2one('hr.employee', string=u'Employé',required=True)
    matricule_dw = fields.Char(u'Matricule DW')
    matricule_dw_prod = fields.Char(u'Matricule DW Prod')
    appels_repondu = fields.Integer(u'Appels Répondus')
    appels_sortant = fields.Integer(u'Appels Sortants')
    temps_connecte = fields.Integer(u'Temps Connecté')
    temps_lunch = fields.Integer(u'Temps en Lunch')
    temps_paie_cms = fields.Float(u'Temps Paie CMS')
    temps_paie_travaille = fields.Float(u'Temps Paie Pretendu',compute='_compute_temps_paie_trvaille')
    corrective_ids = fields.One2many('hr.timesheet.cms.corrective', 'timesheet_cms_id', string='Correctivess')

    @api.depends('temps_paie_cms')
    def _compute_temps_paie_trvaille(self):
        total_hours_worked = 0.0
        for record in self:
            for line in record.corrective_ids:
                if line.type_operation == "add":
                    total_hours_worked += line.nbr_hours
                elif line.type_operation == "substracte":
                    total_hours_worked -= line.nbr_hours
            total_hours_worked+=record.temps_paie_cms
            record.temps_paie_travaille = total_hours_worked

class HrTimesheetCMSCorrective(models.Model):
    _name = "hr.timesheet.cms.corrective"
    _description = "HR Timesheet CMS Corrective"

    user_id = fields.Many2one("res.users", string='User', required=True)
    type_operation = fields.Selection([
        ('add', 'Ajouter'),
        ('substracte', 'Diminuer'),
    ], u"Type Opération")
    nbr_hours = fields.Float(u'Nbre Heures')
    date = fields.Datetime(u'Date Opération')
    timesheet_cms_id = fields.Many2one("hr.timesheet.cms", string='Feuille de Temps CMS', required=True)

    @api.model
    def create(self, vals):
        line = super(HrTimesheetCMSCorrective, self).create(vals)
        line.user_id = self.env.uid
        line.date = fields.Datetime.now()
        return line
