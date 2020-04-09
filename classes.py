from json import dump
from datetime import datetime
from db import get_db


class Endereco:
    rua = None
    cep = None
    numero = None

    def __init__(self, rua, cep, numero):
        self.rua = rua
        self.cep = cep
        self.numero = numero

    def return_dict(self):
        return {'rua': self.rua, 'cep': self.cep, 'numero': self.numero}


class Cliente:
    id = None
    nome = None
    cpf = None
    endereco = None

    def __init__(self, id, nome, cpf, endereco):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

    def mostrar_atributos(self):
        print(f"id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(
            f"Endereço: {self.endereco.rua}, {self.endereco.numero}, {self.endereco.cep}")


class Cliente_para_dict(dict):
    def __init__(self, cliente):
        self['id'] = cliente.id
        self['nome'] = rf"{cliente.nome}"
        self['cpf'] = cliente.cpf
        self['endereco'] = cliente.endereco.return_dict()


class Dict_para_endereco(Endereco):
    def __init__(self, mapa):
        super().__init__(mapa['rua'], mapa['cep'], mapa['numero'])


class Dict_para_cliente(Cliente):
    def __init__(self, mapa):
        super().__init__(
            mapa['id'],
            mapa['nome'],
            mapa['cpf'],
            Dict_para_endereco(mapa['endereco'])
        )


class Sistema:
    clientes = None
    db = None

    def __init__(self):
        self.clientes = list()
        self.db = get_db()
        self.importar_clientes()

    def adicionar_clientes(self):
        id = input("Informe id: ")
        nome = input("Informe Nome: ")
        cpf = input("Informe cpf: ")

        print("-*-Cadastrar endereço-*-")
        rua = input("Informe rua: ")
        cep = input("Informe cep: ")
        numero = input("Informe numero: ")

        found = False
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                found = True

        if not found:
            endereco = Endereco(rua, cep, numero)
            cliente = Cliente(id, nome, cpf, endereco)
            self.clientes.append(cliente)

            cliente_dict = Cliente_para_dict(cliente)
            self.db.clientes.insert_one(cliente_dict)
            print("Cliente cadastrado")
        else:
            print("ERRO! CPF já cadastrado")

    def buscar_cliente_cpf(self, exibir):
        cpf = input("informe cpf: ")
        found = False
        for cliente in self.clientes:
            if cpf == cliente.cpf:
                found = True
                if exibir:
                    cliente.mostrar_atributos()
                    break
                return cliente
        if not found:
            print("Cliente nao encontrado")

    def remover_clientes_cpf(self):
        cpf = input("informe cpf: ")
        found = False
        for cliente in self.clientes:
            if cpf == cliente.cpf:
                self.clientes.remove(cliente)
                found = True

                self.db.clientes.delete_one({"cpf": cpf})
                print("Cliente removido")
                break

        if not found:
            print("Cliente nao encontrado!")

    def atualizar_nome_clientes_cpf(self):
        cpf = input("informe cpf: ")
        found = False
        for cliente in self.clientes:
            if cpf == cliente.cpf:
                self.clientes.remove(cliente)
                cliente.nome = input("Informe o novo nome: ")
                self.clientes.append(cliente)

                self.db.cliente.update_one(
                    {'cpf': cpf}, {"$set": {'nome': cliente.nome}})
                found = True
                print("Cliente atualizado")
                break

        if not found:
            print("Cliente nao encontrado!")

    def buscar_clientes_mesmo_cep(self):
        cep = input("Informe o cep: ")
        found = False
        for cliente in self.clientes:
            if cep == cliente.endereco.cep:
                cliente.mostrar_atributos()
                found = True
        if not found:
            print("Nenhum cliente neste cep encontrado!")

    def todas_as_ruas(self):
        ruas = list()
        for cliente in self.clientes:
            if not cliente.endereco.rua in ruas:
                ruas.append(cliente.endereco.rua)

        for rua in ruas:
            print(rua)

    def importar_clientes(self):
        lista_importacoes = self.db.clientes.find()

        if lista_importacoes:
            for cliente in lista_importacoes:
                self.clientes.append(Dict_para_cliente(cliente))

    def exportar_clientes(self):
        lista_dicts = list()
        data = datetime.now().strftime('%d%m%Y%H%M%S')
        if self.clientes:
            for cliente in self.clientes:
                mapa = Cliente_para_dict(cliente)
                lista_dicts.append(mapa)
            arq = open(f"{data}.json", 'w')
            dump(lista_dicts, arq, indent=4)

    def menu(self):
        while True:
            print(
                '''
<!-- Sistema Cadastro --!>
1 - Adicionar Cliente
2 - Buscar Cliente por cpf
3 - Remover Cliente por cpf
4 - Editar nome de cliente, buscar pelo CPF
5 - Buscar todos os cliente de um mesmo cep
6 - Imprimir todas as ruas dos cliente do sistema
7 - Exportar para json
0 - Sair do Sistema
                '''
            )
            opc = input("--> ")

            if opc == "1":
                self.adicionar_clientes()
            elif opc == "0":
                break
            elif opc == "2":
                self.buscar_cliente_cpf(True)
            elif opc == "3":
                self.remover_clientes_cpf()
            elif opc == "4":
                self.atualizar_nome_clientes_cpf()
            elif opc == "5":
                self.buscar_clientes_mesmo_cep()
            elif opc == "6":
                self.todas_as_ruas()
            elif opc == "7":
                self.exportar_clientes()
            else:
                print("Opcao invalida!")
