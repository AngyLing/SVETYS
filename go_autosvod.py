import autosvod as aut
import pandas as pd


pd.set_option('display.max_columns', 20)


svod_df = aut.add_vars_info(
                            aut.get_raw_db()
                            )

print(svod_df)
# print()
# print(svod_df.info())



# print(list_of_dicts[0])


# TODO: raise exception if english letter
'''
nikolas
nikola
alyosha
styx
svetis
valera
m.a_lina
'''
