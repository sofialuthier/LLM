#reddit yorumlarını combine etmek
import pandas as pd
import datetime as dt
import numpy as np
import os
import sys

def main():
    # reddit api ile yorumları çekmek için fonksiyon
    df1 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\ekonomi_reddit1.csv")
    df2 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\ekonomi_reddit2.csv")
    df3 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\ekonomi_reddit3.csv")
    df4 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\ekonomi_reddit4.csv")
    df5 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\reddit_depresyon.csv")
    df6 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\reddit_finans.csv")
    df7 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\reddit_issizlik.csv")
    df8 = pd.read_csv("C:\\Users\\senel\\OneDrive\\Masaüstü\\LLM\\reddit_yorumlari\\reddit_kariyer.csv")


    combine= pd.concat([df1,df2,df3,df4,df5,df6,df7,df8], axis=0)
    combine.to_csv('combine.csv', index=False)
if __name__ == "__main__":
    main()
    print("Reddit yorumları başarıyla birleştirildi.")