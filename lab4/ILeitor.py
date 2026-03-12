from supabase import *

url = ""
key = ""

supabase: Client = create_client(url,key)
class ILeitor:
    def cadastrarLeitor(self,dadosLeitor):
        response = supabase.table("leitores").insert({"nome" : dadosLeitor.nome , "CPF" : dadosLeitor.cpf, "email" : dadosLeitor.email, "senha" : dadosLeitor.senha, "telefone" : dadosLeitor.telefone})
        return response
