
# Data preparation
---
```bash
paste <(cut -f 2  A_alb.fam) <(cat A_alb.5.Q | tr ' ' '\t') > A_alb.5.Q.tab
```
---




---

# Code Explanation for Admixture Analysis in R

This code provides a step-by-step guide to visualize admixture analysis results on a map of China with pie charts indicating population structure by province, and a structure bar plot for sample clusters.

---

```r
# Install and load necessary library functions
required_packages <- c("sf", "tidyverse", "ggforce", "mapmixture", "gridExtra")

# Check and install the missing packages
for (package in required_packages) {
  if (!require(package, character.only = TRUE)) {
    install.packages(package, dependencies = TRUE)
    library(package, character.only = TRUE)
  }
}
```

### 1. Load Required Libraries

```r
# Load libraries for geographic and data manipulation
library(sf)           # Spatial data handling
library(tidyverse)    # Data manipulation and visualization
library(ggforce)      # Advanced visualizations (used here for pie charts)
library(mapmixture)   # Plotting admixture data
library(gridExtra)    # Arranging multiple plots on one page
```

---

### 2. Load GeoJSON Map Data of China

```r
# Load China's provincial boundaries from a GeoJSON file
china_map_geojson <- st_read("https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json")
```

This loads the China map data from a GeoJSON source, which is used as the base layer for plotting.

---

### 3. Load Admixture Data and Sample-Province Mapping Data

```r
# Load admixture results and province mapping data
A_alb_Q <- read.table("A_alb.5.Q.tab", header = FALSE)
sample_province <- read.csv("sample_province.csv", sep = ",", header = TRUE)
coordinates <- read.csv("china_provinces_lat_lon.csv")
```

Here, `A_alb.5.Q.tab` contains admixture cluster results, `sample_province.csv` links samples to provinces, and `china_provinces_lat_lon.csv` includes geographic coordinates for each province.

---

### 4. Define Column Names for Admixture Data

```r
# Set column names for admixture data
colnames(A_alb_Q) <- c("Ind", paste("Cluster", 1:(ncol(A_alb_Q) - 1), sep = ""))
```

This assigns column names to the admixture data, naming each cluster as "Cluster1," "Cluster2," etc.

---

### 5. Merge Province Information into Admixture Data

```r
# Merge province information to admixture data
admixture1 <- A_alb_Q %>%
  left_join(sample_province, by = "Ind") %>%
  rename(Site = Province) %>%
  select(Site, Ind, everything())
```

We join the sample and province mapping to the admixture data, renaming the "Province" column as "Site."

---

### 6. Calculate Sample Counts per Province and Adjust Size Scale

```r
# Calculate sample count per province and scale the size
site_sample_count <- admixture1 %>%
  group_by(Site) %>%
  summarise(sample_count = n()) %>%
  mutate(pie_size = log1p(sample_count))
```

For visual scaling, we log-transform the sample count to prevent large differences from distorting the plot.

---

### 7. Calculate Mean Population Structure per Province

```r
# Calculate average population structure values by province
admixture_avg <- admixture1 %>%
  group_by(Site) %>%
  summarise(across(starts_with("Cluster"), mean))
```

This calculates the mean admixture proportions for each cluster across samples within a province.

---

### 8. Merge Sample Count Data with Coordinates

```r
# Merge coordinates with sample counts for each province
coordinates_filtered <- coordinates %>%
  filter(Site %in% unique(admixture1$Site)) %>%
  left_join(site_sample_count, by = "Site")
```

Coordinates are merged with sample counts to map locations accurately.

---

### 9. Convert Population Structure to Long Format for Plotting

```r
# Convert population structure to long format for plotting
admixture_long <- admixture_avg %>%
  pivot_longer(cols = starts_with("Cluster"), names_to = "Cluster", values_to = "value") %>%
  left_join(coordinates_filtered, by = "Site")
```

To plot pie charts, we convert the population structure to long format, with "Cluster" and "value" columns.

---

### 10. Plot Map with Pie Charts Showing Admixture Proportions

```r
# Plot map with pie charts indicating population structure
map <- ggplot() +
  geom_sf(data = china_map_geojson, fill = "white", color = "gray") +  # Map of China
  geom_arc_bar(
    data = admixture_long,
    aes(
      x0 = Lon, y0 = Lat, r0 = 0, r = pie_size/2,
      amount = value, fill = Cluster
    ),
    stat = "pie", inherit.aes = FALSE, color = "black"
  ) +
  scale_fill_manual(
    values = c("#FF6B6B", "#4ECDC4", "#556270", "#f1a340", "#998ec3"),
    labels = paste("Ancestry",1:length(unique(admixture_long$Cluster)),sep = "")
  ) +
  coord_sf(xlim = c(73, 135), ylim = c(18, 54), crs = 4326) +
  labs(fill = "Ancestry") +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16),
    legend.position = "right"
  )
```

This block plots China’s map with pie charts representing the population structure proportions per province. Colors indicate different clusters.

---

### 11. Structure Plot for Admixture Data by Site

```r
# Plot structure plot for admixture data
structure_barplot <- structure_plot(
  admixture_df = admixture1,
  type = "structure",
  cluster_cols = c("#FF6B6B", "#4ECDC4", "#556270","#f1a340","#998ec3"),
  site_dividers = TRUE,
  divider_width = 0.4,
  labels = "site",
  flip_axis = FALSE,
  site_ticks_size = -0.05,
  site_labels_size = 2.2
) +
  theme(
    axis.title.y = element_text(size = 8,hjust = 1),
    axis.text.y = element_text(size = 5)
  )
```

The structure plot visualizes individual sample admixture proportions by site, using colors to denote clusters.

---

### 12. Arrange Map and Structure Plot

```r
# Combine map and structure plot in a grid layout
grid.arrange(map, structure_barplot, nrow = 2, heights = c(3,1))
```

This final step combines the map and structure plots, placing them in a 2-row layout with proportions set to emphasize the map.

--- 
