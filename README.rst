===========
Grouped Payment Receipt from Invoices
===========

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2| |badge3|

This module extends the functionality of Odoo’s accounting module to support the generation of a grouped PDF receipt report for payments reconciled with selected customer or vendor invoices. It allows users to select invoices from the same partner in the invoice tree view and generate a consolidated report detailing the associated payments.

**Table of contents**

.. contents::
   :local:

Install
=======

To install this module, you need to:

1. Clone or download the module into your Odoo addons directory.
2. Update the Odoo module list from the user interface (Settings > Modules > Update Modules List).
3. Search for "Grouped Payment Receipt from Invoices" in the Apps menu and click "Install".

No additional non-Python dependencies are required.

Usage
=====

1. Go to **Invoicing > Customer Invoices** or **Invoicing > Vendor Bills**.
2. Select one or more invoices from the same customer or vendor in the tree view.
3. Click the "Grouped Payment Receipt" button in the action bar.
4. A PDF report will be generated, displaying:
   - Partner details (customer or vendor).
   - A table of reconciled payments grouped by date.
   - A table of the selected invoices with their dates and total amounts.

The report title dynamically adjusts to "Recibo" for customer payments or "Orden de pago" for vendor payments.

Known issues / Roadmap
======================

* **Known Issues**: None identified at this stage.
* **Roadmap**: 
  - Add optional filters for payment date ranges in the report generation.
  - Include additional payment details (e.g., withholding taxes) if required by localization.

Bug Tracker
===========

For bug reports or support, please contact us at:
* Help Contact: <support@onlyone.odoo.com>

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne. <https://onlyone.odoo.com/>`_
  
  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne.