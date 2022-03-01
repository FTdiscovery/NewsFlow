const api = require("realtime-newsapi")();
const fs = require("fs");

function renameKey(oldKey, newKey, o) {
  if (oldKey !== newKey) {
    Object.defineProperty(
      o,
      newKey,
      Object.getOwnPropertyDescriptor(o, oldKey)
    );
    delete o[oldKey];
  }
}

api.on("articles", (articles) => {
  console.log("Received new articles!");
  console.log(articles);
  let datetime = new Date();
  let dateString = datetime.toISOString().slice(0, 10);

  let fname = `../realtime-news/${dateString}.json`;
  let articlesJson = fs.readFileSync(fname, "utf-8");

  let articlesArr = JSON.parse(articlesArr);

  articles.forEach((article) => {
    renameKey("url", "link", article);
    renameKey("publishedAt", "date", article);
    articlesArr.push(article);
  });

  articlesJson = JSON.stringify(articlesArr);
  fs.writeFileSync(fname, articlesJson, "utf-8");
});
