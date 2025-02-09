from odoo import models, fields, api
from odoo.exceptions import UserError
class ItiStudent(models.Model):
    _name = "iti.student"

    name = fields.Char(required=True)
    email=fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute="calc_tax")
    address = fields.Text()
    gender = fields.Selection([('m','male'),('f','female')])
    accepted =fields.Boolean()
    level =fields.Integer()
    image =fields.Binary()
    cv =fields.Html()
    login_time =fields.Datetime()
    track_id=fields.Many2one("iti.track")
    track_capacity=fields.Integer(related="track_id.capacity")
    skill_ids=fields.Many2many("iti.skill")
    state=fields.Selection([
        ('applied','Applied'),
        ('first', 'First Interview'),
        ('second','Second Interview'),
        ('passed','Passed'),
        ('rejected','Rejected')
        ], default='applied')
    @api.model
    def create(self, vals):
        new_student = super().create(vals)
        if 'name' in vals and len(vals['name'].split()) >= 2:
            name_split = vals['name'].split()
            new_student.email = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return new_student

    def write(self, vals):
        if "name" in vals and len(vals['name'].split()) >= 2:
            name_split = vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super(ItiStudent, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state not in ['passed', 'rejected']:
                raise UserError("You can't delete students unless they are 'Passed' or 'Rejected'.")
        return super(ItiStudent, self).unlink()

    def change_state(self):
        for record in self:
            if record.state == 'applied':
                record.state = 'first'
            elif record.state == 'first':
                record.state = 'second'
            elif record.state in ['passed', 'rejected']:
                record.state = 'applied'



    def set_passed(self):
         self.state = 'passed'


    def set_rejected(self):
        self.state = 'rejected'

    @api.onchange("gender")
    def _on_change_gender(self):
        if self.gender == 'm':
            self.salary = 10000
        elif self.gender == 'f':
            self.salary = 5000

    @api.depends("salary")
    def calc_tax(self):
        for student in self:
            student.tax =student.salary * 0.20
