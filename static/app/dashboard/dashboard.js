/******************************************************************************
 * dashboard.js
 *
 * Copyright 2016 Marcos Salomão
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version     1.0
 * @author      Marcos Salomão (salomao.marcos@gmail.com)
 *****************************************************************************/


 !function() {

  // data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type
  var tax_data = [
       {"period": "2016-02", "purchase": 3407, "sale": 3660},
       {"period": "2016-01", "purchase": 3351, "sale": 3629},
       {"period": "2015-12", "purchase": 3269, "sale": 2618}
  ];
  Morris.Line({
    element: 'cash_flow-chart',
    resize: true,
    data: tax_data,
    xkey: 'period',
    ykeys: ['purchase', 'sale'],
    labels: ['Purchases', 'Sales']
  });

 }();