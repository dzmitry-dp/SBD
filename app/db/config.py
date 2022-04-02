# version mysql-8.0.28.0

host_name = '127.0.0.1'
user_name = 'postgres'
password = 'postgres'
database_name = 'test'
table_name = 'test'
port = '5432'

# MySQL database
########
table = {
    'table_name': 'test',
    'col_ty': {
        'Proc_Id': 'serial PRIMARY KEY',
        'Proc_Date': 'timestamp with time zone',
        'Proc_Name': 'varchar (255)',
        'Price_ZL': 'numeric (2)', # вещественное число с указанной точностью
        'Price_EUR': 'numeric (2)', # вещественное число с указанной точностью
        'Proc_Link': 'varchar (255)', 
        'Department': 'varchar (25)', 
        'Project': 'varchar (50)',
        'Proc_Comment': 'varchar (255)',
        }
    }

example_values = {
        'Proc_Date': "'2022-03-03'",
        'Proc_Name': "'Трубка шланга для пылесоса с метражом 20мм длина 50 м'",
        'Price_ZL': '84.04',
        'Price_EUR': '64.33',
        'Proc_Link': "'https://allegro.pl/moje-allegro/zakupy/kupione/ddb72880-9b06-11ec-a466-1d12e6b7c649'", 
        'Department': "'Столярка'", 
        'Project': "'Reactor - Prague'",
        'Proc_Comment': "'Не выставляют фактуру'",
    }
########

