angular.module('app', ['ngSanitize'])
.controller('myCtrl', ['$scope','$sce', function($scope,$sce) {
    $scope.count = 0;
    $scope.myFunc = function() {
        $scope.count++;
        
        $scope.group1=   
        ($scope.q1  || 0 )+  ($scope.q2 || 0 ) + ($scope.q3 || 0 ) +($scope.q4 || 0 ) 
        + ($scope.q5  || 0 )+  ($scope.q6 || 0 ) + ($scope.q7 || 0 ) +($scope.q8 || 0 )
        + ($scope.q9  || 0 )+  ($scope.q10 || 0 ) + ($scope.q11 || 0 ) +($scope.q12 || 0 )
        + ($scope.q13  || 0 )+  ($scope.q114 || 0 ) + ($scope.q15 || 0 ) +($scope.q16 || 0 )+($scope.q17 || 0 )
        
        $scope.group2= ($scope.q18  || 0 )+  ($scope.q19 || 0 ) + ($scope.q20 || 0 ) +($scope.q21 || 0 ) +($scope.q22 || 0 ) 
        
        $scope.group3=  ($scope.q23  || 0 )+  ($scope.q24 || 0 ) + ($scope.q25 || 0 )
        $scope.total= $scope.group1+ $scope.group2+ $scope.group3
        
        if  (  $scope.total <=100  &&   $scope.total >= 90  ){
        	$scope.excellent ='<i class="fa fa-check"></i>';
        	$scope.verygood='';
        	$scope.good='';
        	$scope.fair='';
        	$scope.unsatisfied='';
        	
        }
        else if  (  $scope.total <=89  &&   $scope.total >= 80 ){
        	$scope.verygood ='<i class="fa fa-check"></i>';
        	$scope.excellent='';
        	$scope.good='';
        	$scope.fair='';
        	$scope.unsatisfied='';
        }
        else if  (  $scope.total <=79  &&   $scope.total >= 70 ){
        	$scope.good ='<i class="fa fa-check"></i>';
        	$scope.excellent='';
        	$scope.verygood='';
        	$scope.fair='';
        	$scope.unsatisfied='';
        }
        else if  ( $scope.total <=69  &&   $scope.total >= 60 ){
        	$scope.fair ='<i class="fa fa-check"></i>';
        	$scope.excellent='';
        	$scope.verygood='';
        	$scope.good='';
        	$scope.unsatisfied='';
        }
        else if  ( $scope.total < 60 ){
        	$scope.unsatisfied ='<i class="fa fa-check"></i>';
        	$scope.excellent='';
        	$scope.verygood='';
        	$scope.good='';
        	$scope.fair='';
        }
    };
}]);