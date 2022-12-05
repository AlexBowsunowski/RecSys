from itertools import cycle, islice

import pandas as pd

# from rectools import Columns
# from rectools.dataset import Dataset, Interactions


class PopularRecommender:
    def __init__(
        self, max_K=10, days=30, item_column="item_id", dt_column="date"
    ) -> None:
        self.max_K = max_K
        self.days = days
        self.item_column = item_column
        self.dt_column = dt_column
        self.recommendations = []

    def fit(
        self,
        df,
    ):
        min_date = df[self.dt_column].max().normalize() - pd.DateOffset(
            days=self.days
        )  # Нормализованный день к полуночи - 7 дней
        self.recommendations = (
            df.loc[df[self.dt_column] > min_date, self.item_column]
            .value_counts()
            .head(self.max_K)
            .index.values
        )

    def recommend(self, users=None, N=10):
        recs = self.recommendations[:N]
        if users is None:
            return recs
        else:
            return list(islice(cycle([recs]), len(users)))
