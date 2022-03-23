
def generate_tree_schema(article):
    # use get references
    output = "digraph G {"
    output += "\n"
    output += "{ "
    for item in article.citations:
        output += '"'
        output += item["headline"]
        output += '"'
        output += "; "

    output += "}"
    output += " -> "
    output += '"'
    output += article.title
    output += '"'
    output += "\n"

    output += article.title
    output += " -> "
    output += "{"
    for citation in article.citations:
        output += '"'
        output += citation["title"]
        output += '"'
        output += "; "
    output += "}"
    output += "\n"
    output += "}"

    with open("graph1.gv", "w") as outfile:
        outfile.write(output)

    return output

# print(generate_tree_schema())