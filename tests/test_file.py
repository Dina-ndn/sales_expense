from odoo.tests.common import TransactionCase

class TestMyModule(TransactionCase):

    def setUp(self):
        super(TestMyModule, self).setUp()
        # Create necessary records or setup preconditions here
        self.test_partner = self.env['res.partner'].create({
            'name': 'Test Partner'
        })

    def test_create_partner(self):
        """Test partner creation"""
        self.assertEqual(self.test_partner.name, 'Test Partner')

    def test_change_partner_name(self):
        """Test partner name change"""
        self.test_partner.write({'name': 'New Partner Name'})
        self.assertEqual(self.test_partner.name, 'New Partner Name')
