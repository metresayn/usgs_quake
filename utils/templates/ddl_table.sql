DROP TABLE IF EXISTS {{table_name}} CASCADE;
CREATE TABLE IF NOT EXISTS {{table_name}} (
    id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50),
    "property.mag" FLOAT,
    "property.place" VARCHAR(200),
    "property.detail" VARCHAR(200),
    "geometry.type" VARCHAR(50),
    "geometry.coordinates" INTEGER[],
    "generated_at" BIGINT,
    "created_at" TIMESTAMP WITH TIME ZONE,
    "updated_at" TIMESTAMP WITH TIME ZONE
);
DROP TABLE IF EXISTS nearby_cities;
CREATE TABLE IF NOT EXISTS nearby_cities (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50),
    source VARCHAR(50),
    status VARCHAR(50),
    "contents.json_object.contentType" VARCHAR(50),
    "contents.json_object.lastModified" BIGINT,
    "contents.json_object.url" VARCHAR(200)
);
