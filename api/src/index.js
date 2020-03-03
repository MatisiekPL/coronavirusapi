const { ApolloServer, gql } = require('apollo-server');
const { readFileSync } = require('fs');
const mongoose = require('mongoose');
const { GraphQLScalarType } = require('graphql');
const { Kind } = require('graphql/language');
const chrono = require('chrono-node');

const schema = readFileSync(require('path').join(__dirname, '..', 'schema.graphql'), 'UTF-8');
const typeDefs = gql(schema);

const mongoUri = 'mongodb://localhost:27017/coronavirus';
mongoose.connect(mongoUri, { useNewUrlParser: true });
mongoose.Promise = global.Promise;
const db = mongoose.connection;

const io = require('@pm2/io');

const totalReqs = io.counter({
  name: 'Total request count',
  id: 'app/realtime/requests'
});


const resolvers = {
    DateTime: new GraphQLScalarType({
        name: 'DateTime',
        description: 'DateTime',
        parseValue(value) {
            return new Date(value);
        },
        serialize(value) {
            return value.getTime();
        },
        parseLiteral(ast) {
            if (ast.kind === Kind.INT) {
                return new Date(ast.value)
            }
            return null;
        },
    }),
    Query: {
        async countries(parent, { before }, ctx) {
            totalReqs.inc();
            before = before == null ? before = (new Date()).toString() : before = chrono.parseDate(before);
            console.log(before);
            const last = (await db.collection('countries').find({
                time: { $lte: new Date(Date.parse(before)) }
            }).sort({ time: -1 }).toArray())[0];
            if (last == null) return [];
            return (await db.collection('countries').find({
                time: { $lte: new Date(Date.parse(before)), $gte: last['time'] }
            }).toArray()).map(x => {
                x.name = x.country;
                x.fetched_at = x.time;
                x.fetch_time = x.time.toString();
                return x;
            });
        }
    },
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
    console.log(`🚀  Server ready at ${url}`);
});