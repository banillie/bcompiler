Populating templates based on a master spreadsheet
--------------------------------------------------

.. attention::
    The macros explained in the :ref:`macro-handling` section below have been
    replaced with a single macro calledd *UniversalMacro* which will unlock all
    worksheets in the template, run both formatting macros and re-lock sheets
    Use this unless you need to debug a particular step, or you're
    a maschocist...

- Ensure the master spreadsheet is in the ``Documents/bcompiler`` directory.
- Ensure the filename of the master spreadsheet is included in the ``[Master]`` section in ``config.ini``.
- In a command window, run ``bcompiler -a``.
- The resulting files will be created in ``Documents/bcompiler/output``.
- Carry out RAG-colour and Data Validation handling as :ref:`described <macro-handling>`.
- Ensure each sheet and each workbook is protected using a password (either *View*, *Protect Sheet* and
  *View*, *Protect Workbook*, or by running the macro *Protect_All_Sheets*).
- Save the workbook
  
.. warning::
    Make sure the password is retained by all admin users. You will not be able
    to amend the worksheet or workbook if the password is forgotten.


.. _macro-handling:

Handling RAG-colour and Data Validation macros
++++++++++++++++++++++++++++++++++++++++++++++

The BICC data collection process requires that 'blank' templates are sent to
project teams using a number of data validation rules. For example, certain
cells must only be populated by dates or by one a restricted list of options.
This is handled by standard Excel data validation which is mostly set within
the ``bicc_template.xlsm`` form.

However, currently the form contains **two** macros which must be run following a ``bcompiler
-a`` operation to populate all templates from a master spreadsheet:

- *DataVerification*
- *RAG_Conditional*

which provide the template with dropdown choices on certain cells and
conditional formatting on all cells whose value relates to a RAG rating. These
macros are required due to limitations in creating data validation within
``bcompiler`` and its underlying libraries.

Unfortunately, the macros have to be run on each individual file.

**To apply data validation and RAG conditional formatting, do the following:**

1. Run ``bcompiler -a``, as explained above.

Ensure no other Excel files are open on your machine to prevent additional
macros being listed. Then, open each exported populated template in turn, and:

2. Unprotect each sheet (either *Review*, *Unprotect Sheet*, or run the
   *Unprotect_All_Sheets* macro)
3. Run the *DataVerification* macro (*View*, *Macros*, highlight
   *DataVerification*, click *Run*)
4. Run the *RAG_Conditional* macro (*View*, *Macros*, highlight
   *RAG_Conditional*, click *Run*)

.. warning::
    You **must** unlock each worksheet before running the macros, otherwise you
    will encounter a ``Run-time error '1004'`` message in Excel.
    
