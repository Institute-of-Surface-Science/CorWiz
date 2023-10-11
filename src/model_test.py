from models import A13_gabratov

instance = A13_gabratov(200, 5)
print(instance.get_model_name())
print(instance.eval_corrosion_rate())
print(instance.eval_material_loss(5))