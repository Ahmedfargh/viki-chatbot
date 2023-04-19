from neo4j import GraphDatabase
class  person:
    def  __init__(self,name:str,email:str,phone:str,address:str,form_db=False):
        self.name=name
        self.email=email
        self.phone=phone
        self.address=address
        self.id=None
        self._db_auth=("neo4j","ahmedahmed")
        self._GraphDatabase=GraphDatabase.driver("bolt://localhost:11005 ",auth=self.db_auth)
        self._session=self.GraphDatabase.session(connection_acquisition_timeout=999999.9,max_transaction_retry_time=999999999)
        self._form_db=form_db
    def assign_id(self):
        query="MATCH(N)RETURN COUNT(N);"
        data=self._session.run(query)
        self.id=data.values()[0]
        return
class doctor(person):
    def __init__(self,name,email,phone,address,specialist,clinic,form_db=False):
        self.super(name,email,phone,address)
        self.special=specialist
        self.clinic_address=clinic
    def save(self):
        try:
            qeury=""
            if self._form_db:
                qeury="MATCH(person:doctor{name:'"+self.name+"',specialist:'"+self.special+"',clinic_address:'"+self.clinic_address+"',email:'"+self.email+"',phone:'"+self.phone+"',address:'"+self.address+"',id:"+str(self.id)+"})return per"
            else:
                self.assign_id()
                qeury="CREATE(per:doctor{name:'"+self.name+"',specialist:'"+self.special+"',clinic_address:'"+self.clinic_address+"',email:'"+self.email+"',phone:'"+self.phone+"',address:'"+self.address+"',id:"+str(self.id)+"})return person;"
                self._session.run(qeury)
        except:
            raise
    def delete(self):
        try:
            query="MATCH(per:doctor{id:"+str(self.id)+"})detach delete per;";
            self._session.run(query)
        except:
            raise