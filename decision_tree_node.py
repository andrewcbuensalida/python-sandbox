class decision_tree_node:
    def __init__(self, question=None, yes=None, no=None, result=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.result = result


n1 = decision_tree_node(result="General Surgery")
n3 = decision_tree_node(result="Anesthesiology")
n2 = decision_tree_node(question="LOVE operating?", yes=n1, no=n3)
nodes = [n2, n1, n3]

answer = "yes"
if answer == "yes":
    print(n2.yes.result)
else:
    print(n2.no.result)
