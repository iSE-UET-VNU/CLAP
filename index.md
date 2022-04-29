## Detecting False-passing Products and Mitigating their Impact on Variability Fault Localization in Software Product Lines


In a Software Product Line (SPL) system, variability bugs can cause failures in certain products (buggy products), not in the others. In practice, variability bugs are not always exposed, and buggy products can still pass all the tests due to their ineffective test suites (so-called false-passing products). The misleading indications by those false-passing products’ test results can negatively impact variability fault localization performance. In this paper, we introduce CLAP, a novel approach to detect false-passing products in SPL systems failed by variability bugs. Our key idea is to collect failure indications in failing products based on their implementation and test quality. For a passing product, we evaluate these indications, and the stronger indications, the more likely the product is false-passing. The possibility of being false-passing of the product is evaluated based on if it is implemented by a large number of the statements which are highly suspicious in the failing products, and if its test suite is in lower quality compared to the failing products’ test suites. We conducted several experiments to evaluate our false-passing product detection approach on a large benchmark of 14,191 false-passing products and 22,555 true-passing products in 823 buggy versions of the existing SPL systems. The experimental results show that CLAP can effectively detect false-passing and true-passing products with the average accuracy of +90%. Especially, the precision of false-passing product detection by CLAP is up to 96%. This means, among 10 products predicted as false-passing products, more than 9 products are precisely detected. Furthermore, we propose two simple and effective methods to mitigate the negative impact of false-passing products on variability fault localization. These methods can improve the performance of the state-of-the-art variability fault localization techniques by up to 34%.

### Dataset overview


|System       |#Versions |#Fs          |#FPs         |#TPs         |
|-------------|---------:|------------:|------------:|------------:|
|BankAccountTP|       187|        2,055|        2,328|        1,975|
|Elevator     |        41|          217|          326|          195|
|Email        |        69|          553|          587|          723|
|ExamDB       |        77|          201|          127|          288|
|GPL          |       355|        6,612|        9,995|       18,538|
|ZipMe        |        94|          686|          828|          836|
|<b>Total</b> |<b>823</b>|<b>10,433</b>|<b>14,191</b>|<b>22,555</b>|

Note that: 
<dl>
  <dd>#Versions: the number of buggy versions</dd>
  <dd>#Fs: the number of failing products</dd>
  <dd>#FPs: the number of false-passing products</dd>
  <dd>#TPs: the number of true-passing products</dd>
</dl>

Dataset can be found [here](Dataset can be found here: https://tuanngokien.github.io/splc2021/)

### Empirical results

1. Accuracy of false-passing product detection model

<table>
  <thead>
    <tr>
      <th>Classifer</th>
      <th colspan="2">SVM</th>
      <th colspan="2">KNN</th>
      <th colspan="2">Naive Bayes</th>
      <th colspan="2">Logistic Regression</th>
      <th colspan="2">Decision Tree</th>
    </tr>
    <tr>
      <td><b>Lable</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
    </tr>

  </thead>
  <tbody>
  <tr>
    <td><b>Precision</b></td>
    <td>88.16%</td>
    <td><b>94.19%</b></td>
    <td>90.41%</td>
    <td>89.30%</td>
    <td>88.36%</td>
    <td>90.95%</td>
    <td>88.75%</td>
    <td>92.30%</td>
    <td>90.03%</td>
    <td>92.99%</td>
  </tr>
  <tr>
    <td><b>Recall</b></td>
    <td><b>97.09%</b></td>
    <td>78.36%</td>
    <td>93.97%</td>
    <td>83.46%</td>
    <td>95.25%</td>
    <td>79.18%</td>
    <td>95.99%</td>
    <td>79.81%</td>
    <td>96.26%</td>
    <td>82.30%</td>
  </tr>
  <tr>
    <td><b>F1-Score</b></td>
    <td>92.41%</td>
    <td>85.55%</td>
    <td>92.16%</td>
    <td>86.28%</td>
    <td>91.68%</td>
    <td>84.66%</td>
    <td>92.23%</td>
    <td>85.60%</td>
    <td><b>93.04%</b></td>
    <td><b>87.32%</b></td>
  </tr>
  <tr>
      <td><b>Accuracy</b></td>  
      <td colspan="2">90.04%</td>
      <td colspan="2">90.02%</td>
      <td colspan="2">89.21%</td>
      <td colspan="2">89.91%</td>
      <td colspan="2">91.01%</td>
    </tr>
  </tbody>
</table>


2. Mitigating the false-passing products' negative impact on fault localization performance

<table>
  <thead>
    <tr>
      <td rowspan="2"><b>Metric</b></td>
      <td colspan="3">VARCOP</td>
      <td colspan="3">SBFL</td>
    </tr>
    <tr>
      <td><b>Original</b></td>
      <td><b>Removing FPs</b></td>
      <td><b>Adding tests for FPs</b></td>
      <td><b>Original</b></td>
      <td><b>Removing FPs</b></td>
      <td><b>Adding tests for FPs</b></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Tarantula</b></td>
      <td>3.35</td>
      <td>2.52</td>
      <td>2.22</td>
      <td>5.10</td>
      <td>4.75</td>
      <td>4.53</td>
    </tr>
     <tr>
      <td><b>Ochiai</b></td>
      <td>2.39</td>
      <td>2.23</td>
      <td>2.28</td>
      <td>3.00</td>
      <td>2.77</td>
      <td>2.86</td>
    </tr>
     <tr>
      <td><b>Op2</b></td>
      <td>4.31</td>
      <td>4.18</td>
      <td>4.33</td>
      <td>7.04</td>
      <td>6.84</td>
      <td>6.96</td>
    </tr>
     <tr>
      <td><b>Barinel</b></td>
      <td>3.69</td>
      <td>2.83</td>
      <td>2.91</td>
      <td>5.10</td>
      <td>4.74</td>
      <td>4.53</td>
    </tr>
     <tr>
      <td><b>Dstar</b></td>
      <td>2.55</td>
      <td>2.14</td>
      <td>2.19</td>
      <td>3.06</td>
      <td>2.91</td>
      <td>2.98</td>
    </tr>
  </tbody>
</table>

3. Impact of different experimental scenarios

<table>
  <thead>
     <tr>
       <th>Edition</th>
       <th colspan="2">System-based</th>
       <th colspan="2">Version-based</th>
       <th colspan="2">Product-based</th>
       <th colspan="2">Within-system</th>
     </tr>
      <tr>
        <td><b>Lable</b></td>
        <td><b>TP</b></td>
        <td><b>FP</b></td>
        <td><b>TP</b></td>
        <td><b>FP</b></td>
        <td><b>TP</b></td>
        <td><b>FP</b></td>
        <td><b>TP</b></td>
        <td><b>FP</b></td>
      </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Precision</b></td>
      <td>87.51%</td>
      <td>89.42%</td>
      <td>88.16%</td>
      <td>94.19%</td>
      <td>87.53%</td>
      <td>94.27%</td>
      <td>88.73%</td>
      <td>96.12%</td>
    </tr>
    <tr>
      <td><b>Recall</b></td>
      <td>92.16%</td>
      <td>85.83%</td>
      <td>97.09%</td>
      <td>78.36%</td>
      <td>96.97%</td>
      <td>78.26%</td>
      <td>96.29%</td>
      <td>87.02%</td>
    </tr>
    <tr>
      <td><b>F1-Score</b></td>
      <td>89.15%</td>
      <td>86.83%</td>
      <td>92.41%</td>
      <td>85.55%</td>
      <td>92.01%</td>
      <td>85.52%</td>
      <td>92.21%</td>
      <td>91.16%</td>
    </tr>
    <tr>
      <td><b>Accuracy</b></td>
      <td colspan="2">88.44%</td>
      <td colspan="2">90.04%</td>
      <td colspan="2">89.70%</td>
      <td colspan="2">92.29%</td>
    </tr>
  </tbody>
</table>
  
4. Impact of different training data sizes (the number of systems)

<table>
  <thead>
    <tr>
      <th>#Systems</th>
      <th colspan="2">1</th>
      <th colspan="2">2</th>
      <th colspan="2">3</th>
      <th colspan="2">4</th>
      <th colspan="2">5</th>
    </tr>
     <tr>
      <td><b>Lable</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Precision</b></td>
      <td>92.02%</td>
      <td>74.90%</td>
      <td>96.82%</td>
      <td>68.18%</td>
      <td>95.37%</td>
      <td>77.03%</td>
      <td>90.18%</td>
      <td>79.48%</td>
      <td>91.19%</td>
      <td>82.50%</td>
    </tr>
    <tr>
      <td><b>Recall</b></td>
      <td>81.88%</td>
      <td>93.19%</td>
      <td>63.07%</td>
      <td>97.44%</td>
      <td>76.90%</td>
      <td>95.40%</td>
      <td>81.33%</td>
      <td>89.10%</td>
      <td>84.51%</td>
      <td>89.95%</td>
    </tr>
    <tr>
      <td><b>F1-Score</b></td>
      <td>86.65%</td>
      <td>83.05%</td>
      <td>76.38%</td>
      <td>80.23%</td>
      <td>85.14%</td>
      <td>85.24%</td>
      <td>85.53%</td>
      <td>84.02%</td>
      <td>87.72%</td>
      <td>86.06%</td>
    </tr>
    <tr>
      <td><b>Accuracy</b></td>
      <td colspan="2">82.60%</td>
      <td colspan="2">78.47%</td>
      <td colspan="2">85.19%</td>
      <td colspan="2">84.81%</td>
      <td colspan="2">86.95%</td>
    </tr>
  </tbody>
</table>

5. Impact of CLAP's attributes on the false-passing product detection performance

<table>
  <thead>
    <tr>
      <th>Attributes</th>
      <th colspan="2">Product Implementation</th>
      <th colspan="2">Test Adequacy</th>
      <th colspan="2">Test Effectiveness</th>
      <th colspan="2">All</th>
    </tr>
    <tr>
      <td><b>Lable</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
      <td><b>TP</b></td>
      <td><b>FP</b></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Precision</b></td>
      <td>84.69%</td>
      <td>74.80%</td>
      <td>80.45%</td>
      <td>99.07%</td>
      <td>78.74%</td>
      <td>88.50%</td>
      <td>87.47%</td>
      <td>88.29%</td>
    </tr>
     <tr>
      <td><b>Recall</b></td>
      <td>87.71%</td>
      <td>69.69%</td>
      <td>99.74%</td>
      <td>53.69%</td>
      <td>96.59%</td>
      <td>50.18%</td>
      <td>94.66%</td>
      <td>74.82%</td>
    </tr>
     <tr>
      <td><b>F1-Score</b></td>
      <td>86.17%</td>
      <td>72.15%</td>
      <td>89.06%</td>
      <td>69.64%</td>
      <td>86.76%</td>
      <td>64.05%</td>
      <td>90.02%</td>
      <td>81.00%</td>
    </tr>
     <tr>
      <td><b>Accuracy</b></td>
      <td colspan="2">81.52%</td>
      <td colspan="2">83.92%</td>
      <td colspan="2">80.64%</td>
      <td colspan="2">87.71%</td>
    </tr>
  </tbody>
</table>

