# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing det


from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    all_documents = fields.One2many('hr.employee.document', 'employee_ref', string="Document Collaborateur")
    conjoint_documents = fields.One2many('hr.employee.conjoint.document', 'employee_ref', string="Document Conjoint")
    enfants_documents = fields.One2many('hr.employee.enfant.document', 'employee_ref', string="Document Enfant")


class HrEmployeeDocuments(models.Model):
    _name = "hr.employee.document"

    employee_ref = fields.Many2one('hr.employee', string="Employee")
    document = fields.Selection([
        ('cin', 'CIN'),
        ('carte_sejour', 'Carte Séjour'),
        ('photos', 'Photos'),
        ('passport', 'Passport'),
        ('fiche_an', 'Fiche Anthropométrique'),
        ('radio_pul', 'Radio Pulmonaire'),
        ('rib', 'RIB'),
        ('stc', 'STC'),
        ('cnss', 'CNSS'),
        ('attestaion_travail', 'Attestation Travail'),
        ('diplome','Diplome(s)')],
        string="Document")
    date_depot = fields.Date(string=u'Date Dépôt')
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_emp', 'doc_id', 'attach_id3', string=u'Pièce(s) jointe(s)',
                                         help='You can attach the copy of your document', copy=False)

    @api.onchange('document')
    def _onchange_document(self):
        if (self.document):
            self.date_depot = fields.Datetime.now()
        else:
            self.date_depot = False


class HrEmployeeConjointDocuments(models.Model):
    _name = "hr.employee.conjoint.document"

    employee_ref = fields.Many2one('hr.employee', string="Employee")
    conjoint_document = fields.Selection([
        ('cin', 'CIN'),
        ('acte_marriage', 'Acte Marriage'),
        ('photos', 'Photos'),
        ('cnss', 'CNSS'),
        ('attestaion_travail', 'Attestation Travail')],
        string="Document")
    date_depot = fields.Date(string=u'Date Dépôt')
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_emp_conj', 'doc_id', 'attach_id3', string=u'Pièce(s) jointe(s)',
                                         help='You can attach the copy of your document', copy=False)

    @api.onchange('conjoint_document')
    def _onchange_conjoint_document(self):
        if (self.conjoint_document):
            self.date_depot = fields.Datetime.now()
        else:
            self.date_depot = False


class HrEmployeeEnfantDocuments(models.Model):
    _name = "hr.employee.enfant.document"

    employee_ref = fields.Many2one('hr.employee', string="Employee")
    enfants_document = fields.Selection([
        ('acte_naiss', 'Acte Naissance'),
        ('cert_vie_coll', 'Certif Vie Collectif'),
        ('cert_scol', 'Certif Scolarité'),
        ('cert_alloc', 'Certif Allocation Familiale / Mutuelle')],
        string="Document")
    date_depot = fields.Date(string=u'Date Dépôt')
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_emp_enf', 'doc_id', 'attach_id3', string=u'Pièce(s) jointe(s)',
                                         help='You can attach the copy of your document', copy=False)

    @api.onchange('enfants_document')
    def _onchange_enfants_document(self):
        if (self.enfants_document):
            self.date_depot = fields.Datetime.now()
        else:
            self.date_depot = False


class HrEmployeeAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_emp = fields.Many2many('hr.employee.document', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string=u'Pièce(s) jointe(s)', invisible=1)
    doc_attach_emp_conj = fields.Many2many('hr.employee.conjoint.document', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string=u'Pièce(s) jointe(s)', invisible=1)
    doc_attach_emp_enf = fields.Many2many('hr.employee.enfant.document', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string=u'Pièce(s) jointe(s)', invisible=1)