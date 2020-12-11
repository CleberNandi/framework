# encoding: iso-8859-1
import pyad.adobject
import pyad.adgroup
import pyad.adquery as aquery
from win32com.client import GetObject

# obj = pyad.adgroup.ADGroup
class ADGroup(pyad.adgroup.ADGroup):
    def get_members(self):
        return buscar_info(self.dn, self.cn)
    #end def

    def is_member(self, acn, amember_of):
        usuario = ADGroup.from_cn(acn)
        for group in usuario.get_attribute('memberOf'):
            pyADobj = pyad.adgroup.ADObject.from_dn(group)
            if str(pyADobj.get_attribute('cn')[0]) == str(amember_of):
                return True
        return False
    #end def

#end class


def buscar_info(adn,acn):
    SERVIDOR = (adn).replace("CN={},OU=Users,".format(acn), '')
    where_modify="objectClass = '*' and memberOf='CN={},OU=Users,{}' ".format(acn, SERVIDOR,'')
    q = aquery.ADQuery()
    q.execute_query(attributes=["cn"],
                    where_clause=where_modify,
                    base_dn=SERVIDOR)
    # return q.get_results()
    m = []
    for dn in q.get_results():
        novodn = (adn).replace("CN={}".format(acn), "CN={}".format(dn["cn"]))
        pyADobj = pyad.adgroup.ADObject(novodn)
        pyADobj.adjust_pyad_type()
        m.append(pyADobj)
        # m.append(dn["cn"])
    return list((set(m)))  # converting to set removes duplicates
#end def


def remove_from_ldap(group_source, obj_to_remove):
    conn_ldap = GetObject("LDAP://{}".format(group_source.dn))

    if (group_source.is_member(obj_to_remove.cn, group_source.cn)):
        conn_ldap.remove("LDAP://{}".format(obj_to_remove.dn))
    return (group_source.is_member(obj_to_remove.cn, group_source.cn) == False)

# end def

def add_to_ldap(group_source, obj_to_remove):
    conn_ldap = GetObject("LDAP://{}".format(group_source.dn))
    if group_source.is_member(obj_to_remove.cn, group_source.cn) is False:
        conn_ldap.add("LDAP://{}".format(obj_to_remove.dn))

    return (group_source.is_member(obj_to_remove.cn, group_source.cn) == True)
# end def