from config import forbidden

cats_fresh = []

with open('cat-gifs-old.txt', 'r') as f:
    cat_gifs = f.readlines()
    for i in cat_gifs:
      if i.strip() not in cats_fresh:
        if "http" == i.strip()[0:4]:
          if i.strip() not in forbidden:
            cats_fresh.append(i.strip())

with open('cat-gifs.txt', 'w') as f:
    for i in cats_fresh:
       f.write(i + '\n')
      