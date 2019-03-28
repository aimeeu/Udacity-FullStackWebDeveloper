<!---
.. ===============LICENSE_START=======================================================
.. Aimee Ukasick CC-BY-4.0
.. ===================================================================================
.. Copyright (C) Aimee Ukasick. All rights reserved.
.. ===================================================================================
.. This documentation file is distributed by Aimee Ukasick
.. under the Creative Commons Attribution 4.0 International License (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://creativecommons.org/licenses/by/4.0
..
.. This file is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
.. ===============LICENSE_END=========================================================
-->

# Logs Analysis Project
This is the source code for the Logs Analysis Project, which is part of Udacity's Full Stack Web Developer nanodegree. 

# Environment Prerequisites
- This project requires the Virtual Machine as described in ``Project: Logs Analysis Project, Section 3 (Prepare the software and data)``.
The VM should be installed and running. You should have created the news database
and loaded data as instructed by Udacity.

# Installation
Place views_setup.sql and logs_analysis.py in the /vagrant directory where you installed the FullStack VM provided by Udacity.
This is the same directory as the ``Vagrantfile`` location.

# Files
* views_setup.sql: this file contains the scripts that create the database views; please see the bottom
of this README for the contents of view_setup.sql        
* logs_analysis.py: this is the python script that fetches data and prints out the reports
* terminal_output.txt: this file contains the terminal output from running the logs_analysis script

# Usage
* Copy views_setup.sql and logs_analysis.py to the /vagrant directory where you installed the FullStack VM.
* Connect to the VM ``vagrant ssh``
* CD to the /vagrant directory ``cd /vagrant``
* Create the database views ``psql -d news views_setup.sql`` 
* Execute the logs_analysis.py script ``python logs_analysis.py``

Example of terminal commands and successful output:
```bash
vagrant@vagrant:/vagrant$ ls
catalog  forum  logs_analysis.py  newsdata.sql  tournament  Vagrantfile  views_setup.sql
vagrant@vagrant:/vagrant$ psql -d news -f views_setup.sql
CREATE VIEW
CREATE VIEW
CREATE VIEW
CREATE VIEW
CREATE VIEW
vagrant@vagrant:/vagrant$ python logs_analysis.py
Top Three Articles:
	 * "Candidate is jerk, alleges rival" -- 338,647 views
	 * "Bears love berries, alleges bear" -- 253,801 views
	 * "Bad things gone, say good people" -- 170,098 views
Most Popular Authors:
	 * Ursula La Multa -- 507,594 views
	 * Rudolf von Treppenwitz -- 423,457 views
	 * Anonymous Contributor -- 170,098 views
	 * Markoff Chaney -- 84,557 views
Dates With More Than 1.0% Request Errors:
	 * Jul 17, 2016 -- 2.3% errors

('** Total Elapsed Runtime:', '0:0:4')
vagrant@vagrant:/vagrant$ 

```

Contents of view_setup.sql:
    
```sql
    --
    -- Create view used to fetch the 3 most popular articles of all time
    --
    create or replace view view_log_path_trim as
        select path as orig_path, substring(path from 10) as trim_path, time, id
        from log
        where path like '%article%'
        ;
    
    --
    -- Create view used to fetch the most popular article authors of all time
    --
    create or replace view view_author_hits as
      select count(trim.trim_path) as num_of_views, a.name as author
      from view_log_path_trim as trim, articles as art, authors as a
      where trim.trim_path = art.slug
      AND
      art.author = a.id
      group by trim_path, a.name
      order by num_of_views desc
      ;
    
    --
    -- Create views used in fetching the days with more than 1% of requests resulted in an error code
    --
    create or replace view view_log_ok as
      select DATE_TRUNC('day', time) as access_day
      , count(status) as total_hits
      from log
      where status = '200 OK'
      group by access_day
      ;
    
    
    create or replace view view_log_error as
      select DATE_TRUNC('day', time) as access_day
      , count(status) as total_hits
      from log
      where status <> '200 OK'
      group by access_day
      ;
    
    
    create or replace view view_log_error_percent as
      select ok.access_day as ok_day
      , error.access_day as error_day
      , ok.total_hits as ok_total
      , error.total_hits as error_total
      , (ok.total_hits + error.total_hits) as total_daily_hits
      , ROUND(error.total_hits * 100.0 / (ok.total_hits + error.total_hits), 1) as percent_error_hits
      from view_log_ok as ok, view_log_error as error
      where ok.access_day = error.access_day
      ;
```