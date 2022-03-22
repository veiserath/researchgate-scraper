-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-03-22 15:57:34.574

-- tables
-- Table: Article
CREATE TABLE Article (
    Title varchar(150)  NOT NULL,
    URL varchar(200)  NOT NULL,
    Date date  NULL,
    Publisher varchar(100)  NULL,
    Citation_count int  NULL,
    Reference_count int  NULL,
    CONSTRAINT Article_pk PRIMARY KEY (URL)
);

-- Table: ArticleCitation
CREATE TABLE ArticleCitation (
    Main_Article_URL varchar(200)  NOT NULL,
    Citation_Article_URL varchar(200)  NOT NULL,
    CONSTRAINT ArticleCitation_pk PRIMARY KEY (Main_Article_URL, Citation_Article_URL)
);

-- Table: ArticleReference
CREATE TABLE ArticleReference (
    Main_Article_URL varchar(200)  NOT NULL,
    Reference_Article_URL varchar(200)  NOT NULL,
    CONSTRAINT ArticleReference_pk PRIMARY KEY (Main_Article_URL,Reference_Article_URL)
);

-- foreign keys
-- Reference: ArticleCitation_Article1 (table: ArticleCitation)
ALTER TABLE ArticleCitation ADD CONSTRAINT ArticleCitation_Article1
    FOREIGN KEY (Main_Article_URL)
    REFERENCES Article (URL)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: ArticleCitation_Article2 (table: ArticleCitation)
ALTER TABLE ArticleCitation ADD CONSTRAINT ArticleCitation_Article2
    FOREIGN KEY (Citation_Article_URL)
    REFERENCES Article (URL)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: ArticleReference_Article1 (table: ArticleReference)
ALTER TABLE ArticleReference ADD CONSTRAINT ArticleReference_Article1
    FOREIGN KEY (Main_Article_URL)
    REFERENCES Article (URL)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: ArticleReference_Article2 (table: ArticleReference)
ALTER TABLE ArticleReference ADD CONSTRAINT ArticleReference_Article2
    FOREIGN KEY (Reference_Article_URL)
    REFERENCES Article (URL)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

