from pick import pick


def say_question(title, options, table_name):
    def get_label(option):
        return option.get("name" + table_name)

    option, index = pick(options, title, indicator=">", options_map_func=get_label)
    return option["id"]
