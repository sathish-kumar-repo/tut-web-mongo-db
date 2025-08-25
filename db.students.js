db.students.find(
  {},
  { name: 1, exams: { $elemMatch: { score: { $gte: 90 } } }, _id: 0 }
);

db.movies.find({}, { rating: { $elemMatch: { average: { $gt: 9 } } } });
