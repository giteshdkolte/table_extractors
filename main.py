import re

# Define the function for extracting table/view names by checking all possible patterns 
def extractTableViewNames(query):
    # Set containing the table names
    matches = list()
    table_ref_regex = r'(?is)\b(?:(?:(?:CREATE|REPLACE)(?:.*?)(?:VIEW|TABLE))|JOIN|COLLECT STATISTICS ON|INSERT INTO|UPDATE|DELETE FROM|MERGE INTO|TRUNCATE TABLE|REPLACE TABLE|REPLACE VIEW|IMPORT|EXPORT|LOAD|UNLOAD FROM|ANALYZE|REORGANIZE|REBUILD INDEX|RENAME TO|ALTER TABLE|DROP TABLE|GRANT|REVOKE ON|RENAME COLUMN TO|ADD COLUMN|MODIFY COLUMN|DROP COLUMN|ALTER COLUMN|COMMIT|ROLLBACK|SAVEPOINT|RELEASE SAVEPOINT|FETCH|MOVE|COPY FROM|CREATE INDEX|DROP INDEX|ALTER INDEX|DROP VIEW|ALTER VIEW|CREATE PROCEDURE|DROP PROCEDURE|CREATE MACRO|DROP MACRO|ALTER MACRO|CREATE FUNCTION|DROP FUNCTION|ALTER FUNCTION|EXEC)\s+([\w\"\-\`]+(?:\.?[\w\"\-\`]+)+)'
    # Regex for "FROM" keyword
    table_ref_regex_From = r'(?is)\bFROM\s+(?:([\w.\"\-\`]+\s*(?:\w+)?(?:\s*,\s*[\w.\"\-\`]+\s*(?:\w+)?)*))'
    # Getting "FROM" Preceeding by "EXTRACT"
    table_ref_regex_Extract_From = r"(?is)\bEXTRACT\((?:[^()]|\([^)]*\))*FROM\s+([\w\"\-\`]+(?:\.?[\w\"\-\`]+)+)"
    # Regex to find "schema.table" pattern
    schema_table_regex = r'(?is)\b([\w\.\"\-\`]+)\b\s*(?:\w+)?'
 
    # Matches other than "FROM" keyword
    for match in re.finditer(table_ref_regex, query, re.IGNORECASE):
        if match.group(1) is not None:
            matches.append(match.group(1))

    # Matches of "FROM" keyword
    schemas_ext_frm = re.findall(table_ref_regex_Extract_From, query)

    for match in re.finditer(table_ref_regex_From, query, re.IGNORECASE):
        if match.group(1) is not None:
            
            from_catch_split = match.group(1).split(',')
            new_from_catch_split = list()

            for i in from_catch_split:
                refined_from_table_match = re.search(schema_table_regex, i)
                if refined_from_table_match:
                    new_from_catch_split.append(refined_from_table_match.group(1))

        
            for schema_table_match in new_from_catch_split:
                # Logic to eliminate FROM preceeding by EXTRACT
                if schema_table_match not in schemas_ext_frm:
                    matches.append(schema_table_match.replace('"', '').replace('`', ''))
    
    # Handling the MERGE INTO...USING...; this regex will capture the source table used in USING keyword
    using_regex = r"(?is)merge\s+into(.*?)using\s+([\w\"\-\`]+)"
    # Find all matches
    using_matches = re.findall(using_regex, query)
    if using_matches:
        for i in using_matches:
            matches.append(i.replace('"', '').replace('`', ''))

    return list(dict.fromkeys(matches))

if __name__ == "__main__":
    with open(".\\sample\\query.sql") as inp:
        content = inp.read()
        objects = extractTableViewNames(content)
        print(", ".join(objects))
