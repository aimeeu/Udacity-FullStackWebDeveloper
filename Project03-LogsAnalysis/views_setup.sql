-- ===============LICENSE_START=======================================================
-- Aimee Ukasick Apache-2.0
-- ===================================================================================
-- Copyright (C) 2018 Aimee Ukasick. All rights reserved.
-- ===================================================================================
-- This software file is distributed by Aimee Ukasick
-- under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- This file is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
-- ===============LICENSE_END=========================================================

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