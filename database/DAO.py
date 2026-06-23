from database.DB_connect import DBConnect
from model.constructor import Constructor
from model.edge import Edge
from model.peso import Peso
from model.result import Result


class DAO():
    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Constructor(**row, results = {}))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct(s.`year`)
                    from seasons s 
                    order by s.`year` asc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllResults(y1,y2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.constructorId as cId, ra.`year` as year, ra.raceId as rId, r.driverId as dId, r.`position` as position
                    from constructors c, results r, races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId and ra.`year` BETWEEN %s AND %s
                    order by c.constructorId """
        cursor.execute(query, (y1,y2,))

        res = []
        for row in cursor:
            res.append(Result(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdges(y1, y2,idMapC):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c1.id as id1, c2.id as id2
                    from (select distinct(ra.`year`) as year, c.constructorId as id, c.name as name
                    from constructors c, results r, races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId and ra.`year` BETWEEN %s AND %s
                    order by ra.`year` ) c1,
                    (select distinct(ra.`year`) as year, c.constructorId as id, c.name as name
                    from constructors c, results r, races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId and ra.`year` BETWEEN %s AND %s
                    order by ra.`year` ) c2
                    where c1.id > c2.id
                    group by c1.id, c2.id
                    order by c1.id, c2.id"""
        cursor.execute(query, (y1, y2, y1, y2,))

        res = []
        for row in cursor:
            res.append(Edge(idMapC[row["id1"]],idMapC[row["id2"]], 0))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPesi(y1, y2, idMapC):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.constructorId as id, count(*) as numeroGare
                    from constructors c, results r, races ra
                    where c.constructorId = r.constructorId and r.`position` != 0 and r.raceId = ra.raceId and ra.`year` BETWEEN %s AND %s
                    group by c.constructorId 
                    order by c.constructorId"""
        cursor.execute(query, (y1, y2, ))

        res = []
        for row in cursor:
            res.append(Peso(idMapC[row["id"]], row["numeroGare"]))

        cursor.close()
        cnx.close()
        return res


