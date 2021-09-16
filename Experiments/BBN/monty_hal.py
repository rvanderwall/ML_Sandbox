from pomegranate import DiscreteDistribution, ConditionalProbabilityTable
from pomegranate import Node, BayesianNetwork

# Guest will choose random door
guest = DiscreteDistribution({'A': 1./3, 'B': 1./3, 'C': 1./3})

# Prize is in random location
prize = DiscreteDistribution({'A': 1./3, 'B': 1./3, 'C': 1./3})

# Monty has a few rules.
#  He will NOT choose the same door as the guest
#  He will NOT choose the same door as the prize
#  He will randomly choose between the doors that remain
monty = ConditionalProbabilityTable(
        # Guest, Prize, Monty
        [['A', 'A', 'A', 0.0],
         ['A', 'A', 'B', 0.5],
         ['A', 'A', 'C', 0.5],
         ['A', 'B', 'A', 0.0],
         ['A', 'B', 'B', 0.0],
         ['A', 'B', 'C', 1.0],
         ['A', 'C', 'A', 0.0],
         ['A', 'C', 'B', 1.0],
         ['A', 'C', 'C', 0.0],
         ['B', 'A', 'A', 0.0],
         ['B', 'A', 'B', 0.0],
         ['B', 'A', 'C', 1.0],
         ['B', 'B', 'A', 0.5],
         ['B', 'B', 'B', 0.0],
         ['B', 'B', 'C', 0.5],
         ['B', 'C', 'A', 1.0],
         ['B', 'C', 'B', 0.0],
         ['B', 'C', 'C', 0.0],
         ['C', 'A', 'A', 0.0],
         ['C', 'A', 'B', 1.0],
         ['C', 'A', 'C', 0.0],
         ['C', 'B', 'A', 1.0],
         ['C', 'B', 'B', 0.0],
         ['C', 'B', 'C', 0.0],
         ['C', 'C', 'A', 0.5],
         ['C', 'C', 'B', 0.5],
         ['C', 'C', 'C', 0.0]], [guest, prize])


def run_monty_hall():
    s1 = Node(guest, name="guest")
    s2 = Node(prize, name="prize")
    s3 = Node(monty, name="monty")

    model = BayesianNetwork("Monty Hall Problem")
    model.add_states(s1, s2, s3)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.bake()
    print(model.probability([['A', 'A', 'A'],
                             ['A', 'A', 'B'],
                             ['A', 'A', 'C']]))
    print(model.predict([['A', 'A', None], ]))

    # Given I choose A and Monty opened B, what are the chances
    # for the prize behind each door?
    normalizer = model.probability([['A', None, 'B'], ])
    probs = model.probability([['A', 'A', 'B'],
                             ['A', 'B', 'B'],
                             ['A', 'C', 'B']]) / normalizer
    print(f"Probability A:{probs[0]},  B:{probs[1]}, C:{probs[2]}")
