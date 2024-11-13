# file format
[Reference file format](https://github.com/tom-jenkins/mapmixture?tab=readme-ov-file#format)
This map file(.json) is from [Alibaba](https://datav.aliyun.com/portal/school/atlas/area_selector)

```r
head(A_alb_Q)
#>              Ind Cluster1 Cluster2 Cluster3 Cluster4 Cluster5
#> 1   21HNWC2YW0118  0.00001  0.99996  0.00001  0.00001  0.00001
#> 2  21HNSY11YW0543  0.99996  0.00001  0.00001  0.00001  0.00001
#> 3 20NB23MAYYW2795  0.00001  0.00001  0.99996  0.00001  0.00001
#> 4 20NB14JUNYW2900  0.00001  0.00001  0.00001  0.99996  0.00001
#> 5   21HNLS3YW0465  0.00001  0.00001  0.99996  0.00001  0.00001
#> 6   21NBJUNYW1186  0.00001  0.00001  0.00001  0.00001  0.99996
>
```
```r
> head(sample_province)
#>               Ind     Province
#> 1   21HNWC2YW0118     Xinjiang
#> 2  21HNSY11YW0543       Yunnan
#> 3 20NB23MAYYW2795 Heilongjiang
#> 4 20NB14JUNYW2900     Shandong
#> 5   21HNLS3YW0465     Xinjiang
#> 6   21NBJUNYW1186       Yunnan
 >
```



```r
> head(admixture1)
#>          Site             Ind Cluster1 Cluster2 Cluster3 Cluster4 Cluster5
#> 1     Xinjiang   21HNWC2YW0118  0.00001  0.99996  0.00001  0.00001  0.00001
#> 2       Yunnan  21HNSY11YW0543  0.99996  0.00001  0.00001  0.00001  0.00001
#> 3 Heilongjiang 20NB23MAYYW2795  0.00001  0.00001  0.99996  0.00001  0.00001
#> 4     Shandong 20NB14JUNYW2900  0.00001  0.00001  0.00001  0.99996  0.00001
#> 5     Xinjiang   21HNLS3YW0465  0.00001  0.00001  0.99996  0.00001  0.00001
#> 6       Yunnan   21NBJUNYW1186  0.00001  0.00001  0.00001  0.00001  0.99996
> 
```


```r
> head(coordinates)
#>            Site     Lat      Lon
#> 1        Beijing 39.9042 116.4074
#> 2        Tianjin 39.3434 117.3616
#> 3          Hebei 38.0412 114.5149
#> 4         Shanxi 37.8690 112.5480
#> 5 Inner Mongolia 40.8183 111.7491
#> 6       Liaoning 41.8057 123.4291
```

