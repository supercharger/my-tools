angular.module('todoService', [])

	// super simple service
	// each function returns a promise object 
	.factory('Todos', ['$http',function($http) {
		return {
			get : function() {
				return $http.get('/api/todos');
			},
			create : function(todoData) {
				console.log('inside:' + todoData.fileUpload);
				var fd = new FormData();
				fd.append("text", todoData.text);
				fd.append("file", todoData.fileUpload);

				return $http.post('/api/todos', fd, 
            { transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        });
			},
			delete : function(id) {
				return $http.delete('/api/todos/' + id);
			}
		}
	}]);
