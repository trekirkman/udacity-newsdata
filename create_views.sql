--
-- Name: log_path; Type: VIEW; Schema: public; Owner: vagrant
--

CREATE VIEW log_path as
    SELECT path, count(*) AS views
    FROM log
    GROUP BY log.path;

GO

--
-- Name: t_logs; Type: VIEW; Schema: public; Owner: vagrant
--

CREATE VIEW t_logs as
    SELECT date_trunc('day', time) as day, 
    count(*) as total 
    FROM log 
    GROUP BY day;

GO

--
-- Name: e_logs; Type: VIEW; Schema: public; Owner: vagrant
--

CREATE VIEW e_logs as
    SELECT date_trunc('day', time) as day, 
    count(*) as errors 
    FROM log 
    WHERE status like '4%' 
    GROUP BY day;

