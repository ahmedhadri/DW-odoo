# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing det


from odoo import fields, models,api
from odoo.addons import decimal_precision as dp
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

	
class hr_contract(models.Model):
    _inherit = 'hr.contract'

    ##### Autre Avantage #####
    has_phone = fields.Boolean(u'Téléphone', default=False)
    detail_phone = fields.Char(u'Détails')
    date_phone = fields.Date(u'Date de remise téléphone')

    has_pc = fields.Boolean(u'PC Portable', default=False)
    detail_pc = fields.Char(u'Détails', default=False)
    date_pc = fields.Date(u'Date de remise PC Portable', default=False)

    ##### Départ #####
    trial_date_end_1 = fields.Date('First Trial End Date')
    trial_date_end_2 = fields.Date('Second Trial End Date')

    cycle = fields.Selection([('production', 'Production'), ('formation', 'Formation')], string=u'Cycle')
    timming = fields.Selection([('s1', 'S1'), ('s2', 'S2'),('s3', 'S3'), ('s4', 'S4'),('s5', 'S5'), ('s6', 'S6'), ('s7', 'S7')], string=u'Timming')
    nature_depart = fields.Selection([('subi', 'Subi'), ('voulu', 'Voulu')], string=u'Nature de départ')
    mode_depart = fields.Selection([('abandon', 'Abandon de poste'), ('demission', 'Démission'), ('fin_period', 'Fin de période d\'essai')], string=u'Mode de départ')
    raison_depart = fields.Selection([('sante', 'Santé'),
                                      ('retour_pays', 'Retour au pays'),
                                      ('injoignable', 'Injoignable'),
                                      ('opportunite', 'nouvelle opportunité'),
                                      ('linguistique', 'Niveau linguistique'),
                                      ('personnel', 'Problèmes personnelles'),
                                      ('ind_prod', 'Indicateurs de production')], string=u'Raison de départ')
    notes_manager = fields.Text('Notes Manager')
    notes_rh = fields.Text('Notes RH')

    @api.onchange('category_id','type_id','date_start')
    def _onchange_category_id(self):
        """ This function computes trial end period 1 and 2
        """
        if self.date_start:
            if self.type_id.name == "CDI" :
                if self.category_id.name==u'Employé':
                    self.trial_date_end_1 = (datetime.strptime(self.date_start,'%Y-%m-%d') + relativedelta(days=45)).strftime('%Y-%m-%d')
                    self.trial_date_end_2 = (datetime.strptime(self.date_start,'%Y-%m-%d') + relativedelta(months=3)).strftime('%Y-%m-%d')
                if  self.category_id.name=="Cadre":
                    self.trial_date_end_1 = (datetime.strptime(self.date_start,'%Y-%m-%d') + relativedelta(months=3)).strftime('%Y-%m-%d')
                    self.trial_date_end_2 = (datetime.strptime(self.date_start,'%Y-%m-%d') + relativedelta(months=6)).strftime('%Y-%m-%d')


class res_company(models.Model):
    _inherit = 'res.company'
    _name = 'res.company'
   
    plafond_secu = fields.Float(string="Plafond de la Securite Sociale", required=True, default=6000)
    nombre_employes = fields.Integer(string="Nombre d'employes")
    cotisation_prevoyance = fields.Float(string="Cotisation Patronale Prevoyance")
    org_ss = fields.Char(string="Organisme de sécurite sociale")
    conv_coll = fields.Char(string="Convention collective")

class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    
    payment_mode = fields.Char('Mode de paiement', required=False)
  

class hr_employee(models.Model):
    _inherit = 'hr.employee'

	
   
    cin = fields.Char(string="Numéro CIN", required=False)
    matricule_cnss = fields.Char(size=256, string="Numéro CNSS", required=False)
    matricule_cimr = fields.Char(string="Numéro CIMR", required=False)
    matricule_mut = fields.Char(string="Numéro MUTUELLE", required=False)
    num_chezemployeur = fields.Integer(string="Matricule")
    abs = fields.Integer(string="Absence en heures" ,default=0)
    hs25 = fields.Integer(string="Heures sup à 25" ,default=0)
    hs50 = fields.Integer(string="Heures sup à 50",default=0)
    hs100 = fields.Integer(string="Heures sup à 100",default=0)
    av_sal = fields.Integer(string="Avance sur Salaire",default=0)   
    rem_mut = fields.Integer(string="Remboursement Mutuelle",default=0)
   	
	##### information compte bancaire #####

    account_bank_number = fields.Char(string="Numéro de compte", required=False)
    bank_id = fields.Many2one('res.bank', string="Banque", help='Select the Bank from which the salary is going to be paid')

		

		
		
		
	
