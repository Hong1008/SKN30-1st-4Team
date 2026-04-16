CREATE TABLE `stat_ev` (
	`year`	smallint	NOT NULL,
	`region_name`	varchar(50)	NOT NULL,
	`total_ev_count`	int	NULL,
	`total_charger_count`	int	NULL
);

CREATE TABLE `region` (
	`region_name`	varchar(50)	NOT NULL,
	`lat`	double	NULL,
	`lon`	double	NULL,
	`area`	double	NULL
);

CREATE TABLE `qna` (
	`qna_id`	int	NOT NULL,
	`title`	varchar(500)	NULL,
	`year`	smallint	NOT NULL
);

CREATE TABLE `year` (
	`year`	smallint	NOT NULL
);

ALTER TABLE `stat_ev` ADD CONSTRAINT `PK_STAT_EV` PRIMARY KEY (
	`year`,
	`region_name`
);

ALTER TABLE `region` ADD CONSTRAINT `PK_REGION` PRIMARY KEY (
	`region_name`
);

ALTER TABLE `qna` ADD CONSTRAINT `PK_QNA` PRIMARY KEY (
	`qna_id`
);

ALTER TABLE `year` ADD CONSTRAINT `PK_YEAR` PRIMARY KEY (
	`year`
);

ALTER TABLE `stat_ev` ADD CONSTRAINT `FK_year_TO_stat_ev_1` FOREIGN KEY (
	`year`
)
REFERENCES `year` (
	`year`
);

ALTER TABLE `stat_ev` ADD CONSTRAINT `FK_region_TO_stat_ev_1` FOREIGN KEY (
	`region_name`
)
REFERENCES `region` (
	`region_name`
);

