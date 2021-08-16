from pomegranate import DiscreteDistribution, ConditionalProbabilityTable
from pomegranate import Node, BayesianNetwork

cold = DiscreteDistribution({'Yes': 0.1, 'No': 0.9})
allergy = DiscreteDistribution({'Yes': 0.2, 'No': 0.8})


def cough_probability(cold, allergy, cough):
    if cold or allergy:
        return 0.90 if cough else 0.10
    return 0.10 if cough else 0.90


cough = ConditionalProbabilityTable(
        # Cold, Allergy, Cough
        [['No', 'No', 'No', cough_probability(False, False, False)],
         ['No', 'No', 'Yes', cough_probability(False, False, True)],
         ['No', 'Yes', 'No', cough_probability(False, True, False)],
         ['No', 'Yes', 'Yes', cough_probability(False, True, True)],
         ['Yes', 'No', 'No', cough_probability(True, False, False)],
         ['Yes', 'No', 'Yes', cough_probability(True, False, True)],
         ['Yes', 'Yes', 'No', cough_probability(True, True, False)],
         ['Yes', 'Yes', 'Yes', cough_probability(True, True, True)]],
        [cold, allergy])


def itchy_eye_probability(cold, allergy, eye):
    if allergy:
        return 0.90 if eye else 0.1
    return 0.1 if eye else 0.90


itchy_eye = ConditionalProbabilityTable(
        # Cold, Allergy, Itchy Eye
        [['No', 'No', 'No', itchy_eye_probability(False, False, False)],
         ['No', 'No', 'Yes', itchy_eye_probability(False, False, True)],
         ['No', 'Yes', 'No', itchy_eye_probability(False, True, False)],
         ['No', 'Yes', 'Yes', itchy_eye_probability(False, True, True)],
         ['Yes', 'No', 'No', itchy_eye_probability(True, False, False)],
         ['Yes', 'No', 'Yes', itchy_eye_probability(True, False, True)],
         ['Yes', 'Yes', 'No', itchy_eye_probability(True, True, False)],
         ['Yes', 'Yes', 'Yes', itchy_eye_probability(True, True, True)]],
        [cold, allergy])


def run_cough():
    # Causes
    s1 = Node(cold, name="cold")
    s2 = Node(allergy, name="allergy")

    # Observables
    s3 = Node(cough, name="cough")
    s4 = Node(itchy_eye, name="itchy_eye")

    model = BayesianNetwork("Cough Problem")
    model.add_states(s1, s2, s3, s4)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.add_edge(s1, s4)
    model.add_edge(s2, s4)
    model.bake()

    samples = []
    for c in ['No', 'Yes']:
        for a in ['No', 'Yes']:
            for h in ['No', 'Yes']:
                for i in ['No', 'Yes']:
                    samples.append([c, a, h, i])
    print(f"Samples:{model.probability(samples)}")

    # Causes
    print(f"Cold: {model.probability([['Yes', None, None, None]])}")
    print(f"~Cold: {model.probability([['No', None, None, None]])}")
    print(f"Allergy: {model.probability([[None, 'Yes', None, None]])}")
    print(f"~Allergy: {model.probability([[None, 'No', None, None]])}")

    # Observations
    print(f"Cold if Cough: {model.probability([['Yes', None, 'Yes', None]])}")
    print(f"Cold if ~Cough: {model.probability([['Yes', None, 'No', None]])}")
    # print(f"~Cough: {model.probability([[None, None, 'No', None]])}")
    # print(f"Eye: {model.probability([[None, None, None, 'Yes']])}")
    # print(f"~Eye: {model.probability([[None, None, None, 'No']])}")
    #
    # print(model.predict([['No', 'No', None, None], ]))

    # Given I have a cough and itchy eyes
    normalizer = model.probability([[None, None, 'Yes', 'Yes'], ])
    probs = model.probability([['No', None, 'Yes', 'Yes'],
                               ['Yes', None, 'Yes', 'Yes'],
                              ]) / normalizer
    # print(f"Probability No Cold:{probs[0]},  Cold:{probs[1]}")
