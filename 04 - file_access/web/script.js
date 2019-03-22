var app = angular.module('myApp', []);

app.controller('myCtrl', function($scope) {
    window.onload = async function CPU() {
        while(true){
            var valor =  await eel.CPU()();
            $scope.valores = valor.toString();
            document.getElementById("teste").innerHTML = valor;
        }
    }

});



