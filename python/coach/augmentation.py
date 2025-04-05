import cv2
import albumentations as A
import matplotlib.pyplot as plt


def augmentar_imagen(img_path, bbox):

    imagen = cv2.imread(img_path)
    if imagen is None:
        raise ValueError("No se pudo leer la imagen en la ruta proporcionada.")

    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    transform = A.Compose(
        [
            A.AutoContrast(p=1.0),
            A.AdditiveNoise(
                noise_type="gaussian",
                spatial_mode="shared",
                noise_params={"mean_range": (0.0, 0.0), "std_range": (0.05, 0.15)},
            ),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.2),
            A.Rotate(limit=15, p=0.5),
            A.ShiftScaleRotate(
                shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5
            ),
        ],
        bbox_params=A.BboxParams(format="pascal_voc", label_fields=["category_ids"]),
    )

    resultado = transform(image=imagen, bboxes=[bbox], category_ids=[0])
    imagen_transformada = resultado["image"]
    bboxes_transformadas = resultado["bboxes"]

    for box in bboxes_transformadas:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(imagen_transformada, (x1, y1), (x2, y2), (255, 0, 0), 2)

    plt.figure(figsize=(10, 10))
    plt.imshow(imagen_transformada)
    plt.axis("off")
    plt.title("Imagen con Data Augmentation")
    plt.show()

    return imagen_transformada, bboxes_transformadas


path_imagen = "coach/tests/images/frame_0001_normal.jpg"
bounding_box = (
    80.479706,
    420.84103,
    822.28406,
    1171.74,
)  # Ejemplo de coordenadas (x1, y1, x2, y2)
augmentada, bboxes = augmentar_imagen(path_imagen, bounding_box)
