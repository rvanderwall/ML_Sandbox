from GLOM.image_helpers import jpeg_to_8_bit_greyscale, display_image, display_images
from GLOM.Columns import build_columns
from GLOM.ColumnFuncs import add_attention, iterate_column, Weights


def show_level(columns, level, prefix):
    images = [columns[k].stack[level] for k in columns.keys()]
    labels = [(columns[k].abs_x, columns[k].abs_y) for k in columns.keys()]
    display_images(images, labels, f"{prefix} - Level {level}")


def iterate(columns):
    w = Weights()
    for iteration in range(10):
        for k in columns.keys():
            col = columns[k]
            col = add_attention(col, columns, w)
            columns[k] = iterate_column(col, w)

        show_level(columns, 4, f"After iteration {iteration}")


def main():
    print("GLOM running")
    frame = jpeg_to_8_bit_greyscale("Golden-gate-bridge.jpg", (64, 64))
    display_image(frame, "Initial image")
    print(f"Size:{frame.shape}")
    columns = build_columns(frame)
    show_level(columns, 0, "Before iterating")
    iterate(columns)
    for level in range(0, 5):
        show_level(columns, level, "After all iterations")


if __name__ == "__main__":
    main()
