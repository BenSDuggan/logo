import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Variables
logo_path = 'logo.jpg'
cell_size = 25
cell_spacing = 5
default_settings_path = 'config/PhysiCell_settings-backup.xml'
save_settings_path = 'config/PhysiCell_settings.xml'
color_depth = 1
x_num_skip = 50
y_num_skip = 50
rgb_end_range = 3

# Load image
img = plt.imread(logo_path)
#plt.imshow(img)
#plt.show()

# Get domain size
img_size = img.shape[0:-1]
print(img.shape)
# Get pixles with colors
cells = []
#h = 296
#w = 806
#cells.append((h, w, img[h][w][0:-1]*color_depth))
for h in range(0, img_size[0], y_num_skip):
    #break
    for w in range(0, img_size[1], x_num_skip):
        cells.append((h, w, img[h][w][0:rgb_end_range]*color_depth))

# Make XML file
domain_size = img_size
num_cells = 10
num_cells = len(cells)

tree = ET.parse(default_settings_path)
root = tree.getroot()

## Update domain size
#root.find('./domain/x_min').text = str(-1 * domain_size[1] // 2)
#root.find('./domain/x_max').text = str(domain_size[1] // 2)
#root.find('./domain/y_min').text = str(-1 * domain_size[0] // 2)
#root.find('./domain/y_max').text = str(domain_size[0] // 2)

root.find('./user_parameters/num_cells').text = str(num_cells)
cell_node = root.find('./user_parameters')
count = 0

for c in cells:
    node = ET.SubElement(cell_node, 'cell-%s' % count, attrib={'type':'string'})
    node.text = '%d;%d;rgb(%d,%d,%d)' % (c[0], c[1], c[2][0], c[2][1], c[2][2])
    count += 1
    if count == num_cells:
        break
tree.write(save_settings_path)
