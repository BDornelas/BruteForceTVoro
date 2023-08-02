#code adapted from https://rosettacode.org/wiki/Voronoi_diagram#Python

from PIL import Image, ImageDraw
import random
import math
import statistics

#Given a pixel and  collecion of sites, find the closest site to that pixel
def get_voro_cell(pixelx, pixely, sitesx, sitesy):
    j = -1
    dmin= 1000
    for i in range(len(sitesx)):
        d = math.hypot(sitesx[i] - pixelx, sitesy[i] - pixely)
        if d < dmin:
            dmin = d
            j = i
    return j

#Given a number n<10 of sites, get n colorblind friendly colors
def get_colors_specific(n):
    cor_r=[8, 239, 100, 255, 220, 55,240, 150, 125, 0]            #chosen with the help of https://davidmathlogic.com/colorblind/
    cor_g=[224, 96, 71, 153, 38, 160, 228, 175, 95, 0]
    cor_b=[165, 231, 234, 0, 127, 59, 66, 241, 65, 0]
    nr = []
    ng = []
    nb = []
    for i in range(n):
        nr.append(cor_r[i])
        ng.append(cor_g[i])
        nb.append(cor_b[i])
    return nr, ng, nb

# Given a number n of sites, get n random colors
def get_colors_random(n):
    nr = []
    ng = []
    nb = []
    for i in range(n):
        nr.append(random.randrange(256))
        ng.append(random.randrange(256))
        nb.append(random.randrange(256))
    return nr, ng, nb

#Given a picture size, a t value and a collection of sites, brute force plot the t-voronoi regions
def generate_t_voronoi_diagram(width, height, t, sitesx, sitesy, color):
    image = Image.new("RGB", (width, height))           #create image of size (number of pixels) width x height
    putpixel = image.putpixel                           #shortcut for command
    draw = ImageDraw.Draw(image)                        #shortcut for command
    imgx, imgy = image.size

    num_cells = len(sitesx)
    if color==0:
        nr, ng, nb = get_colors_random(num_cells)
    if color==1:
        nr, ng, nb = get_colors_specific(num_cells)

    lista = []
    all_colors_r = []
    all_colors_g = []
    all_colors_b = []
    for y in range(imgy):
        for x in range(imgx):
            del lista[:]                                        #empty list
            j = get_voro_cell(x,y,sitesx,sitesy)
            dmin = math.hypot(sitesx[j]-x, sitesy[j] - y)
            lista.append(j)

            for i in range(num_cells):
                if i==j:
                    continue                                    #next iteration on the for, bec this value already on the list
                d = math.hypot(sitesx[i] - x, sitesy[i] - y)    #distance from pixel to site i
                if d<t:
                    dtotal=0
                else: dtotal=math.sqrt(d*d-t*t)                 #weight the distance with t
                if dtotal < dmin:                               #if distance less than the voro one, it's less than all others
                    lista.append(i)

            del all_colors_r[:]
            del all_colors_g[:]
            del all_colors_b[:]
            for i in range(len(lista)):
                all_colors_r.append(nr[lista[i]])
                all_colors_g.append(ng[lista[i]])
                all_colors_b.append(nb[lista[i]])
            mixed_color_r = int(statistics.mean(all_colors_r))                  #mix all the overlapping colors
            mixed_color_g = int(statistics.mean(all_colors_g))
            mixed_color_b = int(statistics.mean(all_colors_b))
            putpixel((x, y), (mixed_color_r, mixed_color_g, mixed_color_b))
    for i in range(num_cells):                                                  #draw sites
        draw.ellipse((sitesx[i], sitesy[i], sitesx[i] + 10, sitesy[i] + 10), fill=(0, 0, 0), outline=(0, 0, 0))
    image.save("tVoronoiDiagram.png", "PNG")
    image.show()

# user given parameters
image_width=500
image_height=500
t_value=0
color= 1            #select 0 for random colors, 1 for colorblind friendly colors (only works if less than 10 sites)

# hand chosen collection of points
sites_x=[450,50,250,400, 320]
sites_y=[300,240,15,480, 430]

# random collection of points, of size n
n= 10
points_x = []
points_y = []
for i in range(n):
    points_x.append(random.randrange(image_width))
    points_y.append(random.randrange(image_height))

#call function
generate_t_voronoi_diagram(image_width, image_height, t_value, sites_x, sites_y, color)
#generate_t_voronoi_diagram(image_width, image_height, t_value, points_x, points_y, color)
