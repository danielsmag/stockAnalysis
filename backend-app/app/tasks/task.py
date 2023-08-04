from celery import shared_task
from celery.contrib.abortable import AbortableTask
from pandas import DataFrame
from time import sleep
from generalObjects.conn_postgres import ConnPostgres
from app.objects.googleTrends.google_trends_models import GoogleAnalyzes


@shared_task(bind=True, base=AbortableTask)
def update_db(self,kw):
    connPostgres = ConnPostgres(db='analytics',server='airflow')
    connPostgres.create_conn()
    new_kw_df: DataFrame = DataFrame(data=kw, columns=['kw'])
    if not new_kw_df.empty:
        new_kw_df.to_sql('kw', con=connPostgres.get_engine(), schema='google-trends', if_exists='replace', index=False)
        print(new_kw_df)
    connPostgres.close_conn()
    return 'DONE'

@shared_task(bind=True, base=AbortableTask)
def update_all_google_trends(self):
    googleAnalyzes = GoogleAnalyzes()
    print(googleAnalyzes.past_7_days())
    print(googleAnalyzes.past_30_days())
    print(googleAnalyzes.past_3m_days())
    return 'Done'
