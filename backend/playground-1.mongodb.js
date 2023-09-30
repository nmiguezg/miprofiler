/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('mongodbVSCodePlaygroundDB');
db.getCollection('collection').insertMany([
    {
      _id: new UUID("042e4a31-ebd9-465d-a38e-3f736a6113ee"),
      nombre: 'BLM.csv',
      fecha_creacion: 1696066735.625302,
      algoritmo: 'modaresi',
      estadisticas: {
        total_users: 3979,
        age: { '18-24': 9, '25-34': 3961, '35-49': 9, '50-XX': 0 },
        gender: { MALE: 2807, FEMALE: 1172 }
      },
      users: [
        1,2,3,4,5,6,7,7,7,7,7,7,7,7,7,7,7,7,7,,7,7
      ],
      tiempo: 14.382947206497192
    },
    {
      _id: new UUID("38e03b6c-3504-4d1d-9202-efd3943147e1"),
      nombre: 'BLM.csv',
      fecha_creacion: 1696065066.207043,
      algoritmo: 'modaresi',
      estadisticas: {
        total_users: 3979,
        age: { '18-24': 9, '25-34': 3961, '35-49': 9, '50-XX': 0 },
        gender: { MALE: 2807, FEMALE: 1172 }
      },
      tiempo: 14.785660982131958
    }
  ])

// Insert a few documents into the sales collection.
db.getCollection('sales').insertMany([
  { 'item': 'abc', 'price': 10, 'quantity': 2, 'date': new Date('2014-03-01T08:00:00Z') },
  { 'item': 'jkl', 'price': 20, 'quantity': 1, 'date': new Date('2014-03-01T09:00:00Z') },
  { 'item': 'xyz', 'price': 5, 'quantity': 10, 'date': new Date('2014-03-15T09:00:00Z') },
  { 'item': 'xyz', 'price': 5, 'quantity': 20, 'date': new Date('2014-04-04T11:21:39.736Z') },
  { 'item': 'abc', 'price': 10, 'quantity': 10, 'date': new Date('2014-04-04T21:23:13.331Z') },
  { 'item': 'def', 'price': 7.5, 'quantity': 5, 'date': new Date('2015-06-04T05:08:13Z') },
  { 'item': 'def', 'price': 7.5, 'quantity': 10, 'date': new Date('2015-09-10T08:43:00Z') },
  { 'item': 'abc', 'price': 10, 'quantity': 5, 'date': new Date('2016-02-06T20:20:13Z') },
]);

// Run a find command to view items sold on April 4th, 2014.
const salesOnApril4th = db.getCollection('sales').find({
  date: { $gte: new Date('2014-04-04'), $lt: new Date('2014-04-05') }
}).count();

// Print a message to the output window.
console.log(`${salesOnApril4th} sales occurred in 2014.`);

// Here we run an aggregation and open a cursor to the results.
// Use '.toArray()' to exhaust the cursor to return the whole result set.
// You can use '.hasNext()/.next()' to iterate through the cursor page by page.
db.getCollection('sales').aggregate([
  // Find all of the sales that occurred in 2014.
  { $match: { date: { $gte: new Date('2014-01-01'), $lt: new Date('2015-01-01') } } },
  // Group the total sales for each product.
  { $group: { _id: '$item', totalSaleAmount: { $sum: { $multiply: [ '$price', '$quantity' ] } } } }
]);
