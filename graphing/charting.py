import matplotlib.pyplot as plt
import numpy as np

violations = {
    "Encouraging Illegal Activities": ["General", "Mistral", "Haiku"],
    "Promoting Discrimination or Xenophobia": ["Haiku"],
    "Disregarding Privacy": ["Haiku"],
    "Endorsing Harmful Labor Practices": ["Mistral", "Haiku"],
    "Promoting Gender Stereotyping": ["General", "Haiku"],
    "Cultural Insensitivity": ["Haiku"],
    "Defamation or Libel Risks": ["General", "Haiku"]
}

constitutions = ["General", "Mistral", "Haiku"]
counts = {key: [0]*len(constitutions) for key in violations.keys()}

for rule, cons_list in violations.items():
    for cons in cons_list:
        index = constitutions.index(cons)
        counts[rule][index] += 1

# Data preparation
labels = list(counts.keys())
general_counts = [counts[rule][0] for rule in labels]
mistral_counts = [counts[rule][1] for rule in labels]
haiku_counts = [counts[rule][2] for rule in labels]

x = np.arange(len(labels)) 
fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x, general_counts, label='General', color='blue')
rects2 = ax.bar(x, mistral_counts, bottom=general_counts, label='Mistral', color='green')
general_plus_mistral = [g + m for g, m in zip(general_counts, mistral_counts)]
rects3 = ax.bar(x, haiku_counts, bottom=general_plus_mistral, label='Haiku', color='red')

ax.set_xlabel('Violated Rules')
ax.set_ylabel('Count of Violations')
ax.set_title('Count of Missed Violations by Constitution (Stacked)')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.legend()

fig.tight_layout()

plt.show()
