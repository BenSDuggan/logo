import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Variables
logo_path = 'logo.jpg'
default_settings_path = 'config/PhysiCell_settings-backup.xml' #PhysiCell settings that don't our settings get restored from
save_settings_path = 'config/PhysiCell_settings.xml' #PhysiCell settings to use
save_cell_path = 'config/cells.txt' #x,y,radius,color for each cell (currently unused)
cell_radius = 2.5
color_depth = 1
x_num_skip = 5
y_num_skip = 5
x_margin = 50
y_margin = 50
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
        cells.append((h+y_margin, w+x_margin, img[h][w][0:rgb_end_range]*color_depth))

# Make XML file
domain_size = [img_size[0] + 2*y_margin, img_size[1] + 2*x_margin]
domain_midpoint = [domain_size[0] // 2, domain_size[1] // 2]
#num_cells = 10
num_cells = len(cells)

tree = ET.parse(default_settings_path)
root = tree.getroot()

## Update domain size
root.find('./domain/x_min').text = str(-1 * domain_size[1] // 2)
root.find('./domain/x_max').text = str(domain_size[1] // 2)
root.find('./domain/y_min').text = str(-1 * domain_size[0] // 2)
root.find('./domain/y_max').text = str(domain_size[0] // 2)

root.find('./user_parameters/num_cells').text = str(num_cells)
user_param_root = root.find('./user_parameters')
ET.SubElement(user_param_root, 'cell-def-file', attrib={'type':'string'}).text = save_cell_path

tree.write(save_settings_path)

f = open(save_cell_path, 'w')
count = 0

for c in cells:
    f.write('%d;%d;%.2f;rgb(%d,%d,%d)\n' % (domain_midpoint[0]-c[0], c[1]-domain_midpoint[1], cell_radius, c[2][0], c[2][1], c[2][2]))
    count += 1
    if count == num_cells:
        break

f.close()

print("Total agents: %d" % len(cells))
