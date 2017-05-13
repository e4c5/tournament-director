var app = angular.module('app', ['ngResource','ngRoute'])

app.config(['$routeProvider', function ($routeProvider) {

  $routeProvider
    .when('/', {
      template: '',
      controller: 'main'
    })
    .when('/players/:player_id', {
      templateUrl: 'static/player.html',
      controller: 'players-view'
    })
    .when('/rounds/:round_id', {
        templateUrl: 'static/round.html',
        controller: 'rounds-view',
    })
    .when('/result/:result_id', {
        templateUrl: 'static/round.html',
        controller: 'rounds-view',
    })
    .when('/standing/:standing_id', {
        templateUrl: 'static/standing.html',
        controller: 'rounds-view',
    })


}]);

app.factory('PlayerService', function($resource){
    return $resource('/api/players/:player_id',{player: "@player" });
});
app.factory('RoundService', function($resource){
    return $resource('/api/round/:round_id',{round: "@round" });
});
app.factory('ResultService', function($resource){
    return $resource('/api/result/:result_id',{result: "@result" });
});
app.factory('StandingService', function($resource){
    return $resource('/api/standing/:standing_id',{round: "@standing" });
});


app.controller('main', ['$scope','$http','TeamService','$location', 
                function($scope, $http, TeamService, $location) {
    
    $scope.teams = TeamService.query();
    
    $scope.add = function () {
        TeamService.save('/api/teams', {'name': $scope.name},
            function(response){
                $scope.teams.push(response)
            }
        );
    };

    $scope.remove = function (team) {
        TeamService.remove({team_id: team._id}, function(response) {
            $scope.teams.splice($scope.teams.indexOf(team),1);
        });
    };

    $scope.members = function(team) {
        $location.path("/teams/" + team._id);
    }
        
    
}]);

app.controller('member-view', ['$scope', 'TeamService','$routeParams', function ($scope, TeamService, $routeParams) {
    $scope.details = TeamService.get({team_id: $routeParams.team_id}, function(response){
        console.log(response);
    }, function(reject) {
        console.log(reject);
    });

}]);

app.controller('edit-view', ['$scope', 'EmployeeService','$routeParams', function ($scope, EmployeeService, $routeParams) {
    $scope.employee =  EmployeeService.get({employee_id: $routeParams.employee_id});
}]);
