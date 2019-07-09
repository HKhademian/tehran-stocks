from tehran_stocks.config import *
from sqlalchemy.orm import relationship
import pandas as pd


class Stocks(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    group_name = Column(String)
    group_code = Column(Integer)
    instId = Column(String)
    insCode = Column(String)
    code = Column(String, unique=True)
    sectorPe = Column(Float)
    shareCount = Column(Float)
    estimatedEps = Column(Float)
    baseVol = Column(Float)
    prices = relationship("StockPrice", backref="stock")

    def price_df(self):
        query = f"select * from stock_price where code = {self.code}"
        df = pd.read_sql(query, engine)
        df["date"] = pd.to_datetime(df["dtyyyymmdd"], format="%Y%m%d")
        self.df = df
        return df

    def update(self):
        from tehran_stocks import downloader

        try:
            res = downloader.update_stock_price(self.code)
            return res
        except:
            return False

    def check_price(self):
        try:
            self.df
        except:
            self.price_df()

    def summary(self):
        self.check_price()
        df = self.df
        sdate = df.date.min().strftime("%Y%m%d")
        edate = df.date.max().strftime("%Y%m%d")

        print(f"Start date: {sdate}")
        print(f"End date: {edate}")
        print(f"Total days: {len(df)}")

    def __repr__(self):
        return f"{self.title}-{self.name}-{self.group_name}"

    def __str__(self):
        return self.name


class StockPrice(Base):
    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True)
    code = Column(String, ForeignKey("stocks.code"))
    ticker = Column(String)
    date = Column("dtyyyymmdd", Integer)
    first = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    value = Column(Integer)
    vol = Column(Integer)
    openint = Column(Integer)
    per = Column(String)
    open = Column(Float)
    last = Column(Float)

    def __repr__(self):
        return self.stock.name

