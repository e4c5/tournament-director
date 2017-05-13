var app = angular.module('app', ['ngResource','ngRoute'])

app.config(['$routeProvider', function ($routeProvider) {

  $routeProvider
    .when('/', {
      templateUrl: 'static/html/player.html',
      controller: 'main'
    })
    .when('/players/:player_id', {
      templateUrl: 'static/html/player.html',
      controller: 'main'
    })
    .when('/rounds/:round_id/', {
        templateUrl: 'static/html/round.html',
        controller: 'rounds-view',
    })
    .when('/rounds/', {
        templateUrl: 'static/html/round.html',
        controller: 'rounds-view',
    })
    .when('/results/:result_id', {
        templateUrl: 'static/html/result.html',
        controller: 'results-view',
    })

    .when('/results/', {
        templateUrl: 'static/html/result.html',
        controller: 'results-view',
    })
    .when('/standings/:standing_id', {
        templateUrl: 'static/html/standing.html',
        controller: 'standings-view',
    })


}]);

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.factory('PlayerService', function($resource){
    return $resource('/api/players/:player_id',{player: "@player" });
});
app.factory('Rounds', function($resource){
    return $resource('/api/rounds/:round_id',{round: "@round" },
           {results: { method: 'GET', url: 'results' }}
    );
});
app.factory('Results', function($resource){
    return $resource('/api/results/:result_id',{result: "@result" });
});
app.factory('StandingsService', function($resource){
    return $resource('/api/standings/:standing_id',{standing: "@standing" });
});


app.controller('main', ['$scope','$http','PlayerService','$location', 
                function($scope, $http, PlayerService, $location) {
    
    $scope.players = PlayerService.query();
    $scope.sortColumn = 'name'
    $scope.sortReverse = false;

    $scope.add = function () {
        PlayerService.save('/api/players', {'name': $scope.player.name, 'rating': $scope.player.rating},
            function(response){
                $scope.players.push(response)
            }
        );
    };

    $scope.remove = function (team) {
        PlayerService.remove({team_id: team._id}, function(response) {
            $scope.teams.splice($scope.teams.indexOf(team),1);
        });
    };

    $scope.members = function(team) {
        $location.path("/players/" + player._id);
    }
        
    
}]);

app.controller('rounds-view', ['$scope', 'Rounds','$routeParams', function ($scope, Rounds, $routeParams) {
    if ($routeParams.hasOwnProperty("round_id")) {
    
    }
    else {
        $scope.rounds = Rounds.query();
    }
    $scope.add = function () {
        Rounds.save({},
            function(response){
                $scope.rounds.push(response)
            },
            function(err, response) {
                console.log(err);
                console.log(response);
            }
        );
    };
}]);

app.controller('standings-view', ['$scope', 'StandingsService','$routeParams', function ($scope, StandingsService, $routeParams) {
    console.log('standing');
    $scope.employee = StandingsService.get({standing_id: $routeParams.round_id});
}]);

app.controller('results-view', ['$scope', 'Results','$routeParams', function ($scope, Results, $routeParams) {
    
    $scope.results = Results.query({result_id: $routeParams.round_id});
}]);
