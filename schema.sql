-- PSql
-- on database gentchu

CREATE TABLE IF NOT EXISTS tb_portifolios(
	user_id BIGINT NOT NULL UNIQUE,
	-- username varchar(200) NOT NULL,
	distro TEXT NOT NULL,
	langs TEXT[5] NOT NULL,
	github_link TEXT NOT NULL,
	custom_link TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_distros(
	distro TEXT NOT NULL UNIQUE,
	img_path TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS tb_cursed_users(
	user_id BIGINT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tb_links(
	user_id BIGINT NOT NULL,
	link_name TEXT NOT NULL,
	url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_coordinates_mc(
	user_id BIGINT NOT NULL,
	save_name TEXT NOT NULL,
	x_val FLOAT NOT NULL,
	y_val FLOAT DEFAULT 64,
	z_val FLOAT NOT NULL
);


CREATE TABLE IF NOT EXISTS tb_coffee_counter(
	user_id BIGINT NOT NULL,
	total INTEGER NOT NULL DEFAULT 1,
	last_cup TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
