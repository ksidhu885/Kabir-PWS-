import node
import Neural_Network_en_gewichten
import random

class Brain:
    def __init__(self, inputs, clone=False):
        self.nodes = []
        self.connections = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
            #create nodes
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            #bias node
            self.nodes.append(node.Node(3))
            self.nodes[3].layer = 0
            #output node
            self.nodes.append(node.Node(4))
            self.nodes[4].layer = 1
            #connectinos
            for i in range(0, 4):
                self.connections.append(Neural_Network_en_gewichten.Connection(self.nodes[i], self.nodes[4], random.uniform(-1, 1)))

    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for j in range(0, len(self.connections)):
            self.connections[j].from_node.connections.append(self.connections[j])

    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        self.nodes[3].output_value = 1 

        for i in range(0, len(self.net)):
            self.net[i].activate()

        output_value = self.nodes[4].output_value

        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value
    

    
# def feed_forward(self, vision) neemt de inputwaarden (vision) en zet deze in de inputknooppunten van het brein.
# Vervolgens activeert het elk knooppunt in het netwerk in de juiste volgorde en retourneert het de outputwaarde van het outputknooppunt.
# Dit is essentieel voor het laten functioneren van het neurale netwerk, omdat het de manier is waarop de AI beslissingen neemt op basis van wat het "ziet".
# de output value = de beslissing van de AI, bijvoorbeeld of de vogel moet flappen of niet.
# de input is wat de AI "ziet", zoals de afstand tot de pijpen.
    def clone(self):
        clone = Brain(self.inputs, True)

        for n in self.nodes:
            clone.nodes.append(n.clone())

        for d in self.connections:
            clone.connections.append(d.clone(clone.getNode(d.from_node.id), clone.getNode(d.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone
# def clone(self) maakt een kopie van het brein, inclusief alle knooppunten en verbindingen.
# Dit is belangrijk voor het creëren van nieuwe vogels in de volgende generatie, zodat ze kunnen erv
    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n
# def getNode(self, id) zoekt een knooppunt in het brein op basis van zijn ID en retourneert dat knooppunt.
# Dit is handig bij het klonen van het brein, zodat de verbindingen correct kunnen worden hersteld tussen de gekloonde knooppunten.
    def mutate(self):
        if random.uniform(0, 1) < 0.9: 
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()
                # Def mutate(self) zorgt ervoor dat de gewichten van de verbindingen in het brein met een kans van 90% worden aangepast.
                # Dit helpt om variatie in het gedrag van de AI te introduceren, wat belangrijk is voor het leerproces.
         
    def mutate_weight(self):
        if random.uniform(0, 1) < 0.01:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1)/10
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1       # het is 90% omdat je wilt dat de meeste gewichten worden aangepast, maar niet allemaal, zodat er nog steeds enige consistentie is in het gedrag van de AI.