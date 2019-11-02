.. image:: https://github.com/sork93/AJPOC/blob/master/ajpoc/resources/AJPOC_900_400_px.png?raw=true
   :width: 900 px
   :height: 400 px
   :align: center
   :scale: 100 %
   :target: https://github.com/sork93/AJPOC
   :alt: AJPOC

|

**AJPOC** stands for **A**\ irbus **J**\ obs **PO**\ rtal **C**\ rawler, and therefore this project aims to
implement a customizable web crawler for the vacancies listed in the Airbus careers portal.

.. image:: https://img.shields.io/github/license/cpsancha/AJPOC?style=flat
   :target: https://www.gnu.org/licenses/gpl-3.0.html
   :alt: GitHub

.. image:: https://img.shields.io/travis/cpsancha/AJPOC.svg?branch=master?style=flat&logo=travis
   :target: https://travis-ci.org/cpsancha/AJPOC
   :alt: Travis CI

.. image:: https://img.shields.io/github/issues/cpsancha/AJPOC?style=flat&logo=github
   :target: https://github.com/cpsancha/AJPOC/issues
   :alt: GitHub issues

.. image:: https://img.shields.io/codecov/c/github/cpsancha/AJPOC/master?style=flat&logo=Codecov
   :target: https://codecov.io/gh/cpsancha/AJPOC
   :alt: Codecov

.. image:: https://img.shields.io/codacy/grade/d0b14262d7c0464a8daed8370b204ee9/master?style=flat&logo=Codacy
   :target: https://www.codacy.com/app/cpsancha/AJPOC
   :alt: Codacy

.. image:: https://img.shields.io/badge/status-in%20development-blue

***************
Project stages:
***************

Stage 1 (Work-in-progress)
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Implementation of the `Scrapy spider <https://doc.scrapy.org/en/latest/topics/spiders.html>`_ capable of:

  - Following the *"Next Page"* hyperlink in the vacancies listing pages.
  - Following the vacancies links to access to its details.
  - Parse the vacancies contents and show them formatted in the terminal.
- Customizable logging capabilities both to terminal and to file.

Stage 2 (TODO)
^^^^^^^^^^^^^^
- Implement the necessary classes for storing the information of the parsed "*vacancies*" objects into models.
- Implement a custom `Scrapy pipeline <https://doc.scrapy.org/en/latest/topics/item-pipeline.html>`_ to process the
  parsed data into this new objects.
- Adapt the `spider <https://doc.scrapy.org/en/latest/topics/spiders.html>`_ to use the new `pipeline
  <https://doc.scrapy.org/en/latest/topics/item-pipeline.html>`_.

Stage 3 (TODO)
^^^^^^^^^^^^^^
- Implement the mapping of the objects into a relational database structure (most likely by the use of a database
  agnostic Object-Relational-Mapper like `SQL Alchemy <https://www.sqlalchemy.org/>`_).
- Provide persistence for the scraped data by storing the obtained information into a relational database:

  - Connect to an existing DB (or create it and connect if it does not exist) on startup.
  - Adapt the `pipeline <https://doc.scrapy.org/en/latest/topics/item-pipeline.html>`_ to add the parsed data
    into the database.

Stage 4 (TODO)
^^^^^^^^^^^^^^
- Compute the deltas with the previous existing data in the DB.

  - Look for the presence of an object with the same *Id* in the DB.
  - If the object already exists and no modifications exist, skip it.
  - If the object already exists and any field has been modified, update it and mark it as *"Modified"*.
  - If the object is not present, add it and mark it as *"Added"*.
  - If an object used to exit, but it is not present any longer, remove it and mark it as *"Deleted"*.
  - Provide a summary report with the *"Added"*, *"Modified"* and *"Deleted"* elements.

Stage 5 (TODO)
^^^^^^^^^^^^^^
- Implement a filtering mechanism so the user can tweak the vacancies processed:

  - Add support for the filters of the Airbus Job Site.
  - Add support for custom filters based on keywords of the vacancies contents.

Stage 6 (TODO)
^^^^^^^^^^^^^^
- Provide a push notification mechanism through telegram with the
  `python-telegram-bot <https://python-telegram-bot.org/>`_.

  - Create a new telegram bot.
  - Integrate the `python-telegram-bot <https://python-telegram-bot.org/>`_ API in the code.
  - Send messages to the subscribed users with the report result after the scraping completion.

Stage 7 (TODO)
^^^^^^^^^^^^^^
- At this stage, the program should be capable of running in a loop on a Raspberry Pi while sending notifications
  to the user every time a new vacancy is published, modified or removed.
- Testing, tweaking and bug fixing...