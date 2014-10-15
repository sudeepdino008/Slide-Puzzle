/*
Project name : N_Puzzle
Created on : Tue Jul 29 09:19:24 2014
Author : Anant Pushkar
https://www.hackerrank.com/challenges/n-puzzle
*/
#include<iostream>
#include<cstring>
#include<cstdio>
#include<deque>
#include<queue>
#include<utility>
#include<vector>
#include<climits>
#include<algorithm>
#include<stack>
#include<set>
using namespace std;
bool debug=false;
typedef long long int lld;
typedef unsigned long long int llu;
struct State{
	vector<vector<int> > grid;
	int size , x , y , score;
	deque<string> path;
	
	State():
	size(0),
	x(-1),
	y(-1),
	score(0),
	grid(vector<vector<int> >(0 , vector<int>(0,0))){
		
	}
	
	State(int k):
	size(k),
	x(-1),
	y(-1),
	score(0),
	grid(vector<vector<int> >(k , vector<int>(k,0))){
		
	}
	
	State(const State &s):
	size(s.size),
	x(s.x),
	y(s.y),
	score(s.get_score()),
	path(deque<string>(s.path.begin() , s.path.end())),
	grid(vector<vector<int> >(s.grid.size() , vector<int>(s.grid.size()))){
		for(int i=0;i<size;++i){
			for(int j=0;j<size;++j){
				grid[i][j] = s.grid[i][j];
			}
		}
	}
	
	bool operator==(const State &s2){
		if(this->size!=s2.size){
			return false;
		}
		for(int i=0;i<size;++i){
			for(int j=0;j<size;++j){
				if(this->grid[i][j] != s2.grid[i][j]){
					return false;
				}
			}
		}
		return true;
	}
	/*
	inline bool operator<(const State &s2){
		return this->get_score() < s2.get_score();
	}
	
	inline bool operator>(const State &s2){
		return this->get_score() > s2.get_score();
	}*/
	
	void print() const {
		for(int i=0;i<size;++i){
			for(int j=0;j<size;++j){
				cout<<grid[i][j]<<" ";
			}
			cout<<endl;
		}
		cout<<"Score : "<<get_score()<<endl;
		cout<<endl;
	}
	
	inline int get_score() const{
		return score;
	}
};
struct compare{
	bool operator()(const State &s1 , const State &s2){
		return s1.get_score() > s2.get_score();
	}
};

struct compare_structure{
	bool operator()(const State &s1 , const State &s2){
		if(s1.size<s2.size){
			return true;
		}
		if(s1.size>s2.size){
			return false;
		}
		for(int i=0;i<s1.size;++i){
			for(int j=0;j<s2.size;++j){
				if(s1.grid[i][j]<s2.grid[i][j]){
					return true;
				}
				if(s1.grid[i][j]>s2.grid[i][j]){
					return false;
				}
			}
		}
		return false;
	}
};

void exchange(int &a , int &b){
	a = a^b;
	b = a^b;
	a = a^b;
}
class Solver{
	int k;
	State init_state , final_state;
	deque<string> path;
	set<State , compare_structure> state_set;
	vector<pair<int,int> > pos;
	State transform(const State &s , string move){
		State next_state = s;
		int x = s.x , y = s.y;
		
		if(debug)cout<<"Making move : "<<move<<endl;
		if(move == "right"){
			exchange(next_state.grid[x][y] , next_state.grid[x][y+1]);
			next_state.y = y+1;
		}else if(move == "left"){
			exchange(next_state.grid[x][y] , next_state.grid[x][y-1]);
			next_state.y = y-1;
		}else if(move == "up"){
			exchange(next_state.grid[x][y] , next_state.grid[x-1][y]);
			next_state.x = x-1;
		}else if(move == "down"){
			exchange(next_state.grid[x][y] , next_state.grid[x+1][y]);
			next_state.x = x+1;
		}
		
		if(debug)cout<<"initialising score"<<endl;
		next_state.score = get_score(next_state , final_state);
		
		if(debug)cout<<"Pushing move to path history"<<endl;
		next_state.path.push_back(move);
		
		if(debug){
			cout<<"Next State"<<endl;
			next_state.print();
		}
		return next_state;
	}
	int get_score(const State &s , const State &final_state){
		//return 0;
		int count=0;
		for(int i=0;i<s.size;++i){
			for(int j=0;j<s.size;++j){
				count += s.grid[i][j] != final_state.grid[i][j] ? 1 : 0;
			}
		}
		int dist=0;
		for(int i=0;i<s.size;++i){
			for(int j=0;j<s.size;++j){
				dist += abs(i-pos[s.grid[i][j]].first) + abs(j-pos[s.grid[i][j]].second);
			}
		}
		return (count>dist ? count : dist) + s.path.size();
	}
	bool push_to_pq(State &next , priority_queue<State, vector<State> , compare> &pq){
	//bool push_to_pq(State &next , stack<State> &pq){
		//next.score = get_score(next , final_state);
		pq.push(next);
		state_set.insert(next);
		if(next==final_state){
			path = deque<string>(next.path.begin() , next.path.end());
			return true;
		}
		return false;
	}
	bool expand(const State &s , priority_queue<State, vector<State> , compare> &pq){
	//bool expand(const State &s , stack<State> &pq){
		if(debug){
			cout<<"-------------------------------\nExpanding :"<<endl;
			s.print();
		}
		State next;
		deque<State> next_list;
		if(s.y+1<k){
			next = transform(s , "right");
			if(state_set.find(next)==state_set.end()){
				if(debug)cout<<"Pushing state to priority queue"<<endl;
				if(push_to_pq(next , pq)){
					return true;
				}
				//next_list.push_back(next);
			}else{
				if(debug)cout<<"State visited previously"<<endl;
			}
		}
		if(s.y-1>-1){
			next = transform(s , "left");
			if(state_set.find(next)==state_set.end()){
				if(debug)cout<<"Pushing state to priority queue"<<endl;
				if(push_to_pq(next , pq)){
					return true;
				}
				//next_list.push_back(next);
			}else{
				if(debug)cout<<"State visited previously"<<endl;
			}
		}
		if(s.x-1>-1){
			next = transform(s , "up");
			if(state_set.find(next)==state_set.end()){
				if(debug)cout<<"Pushing state to priority queue"<<endl;
				if(push_to_pq(next , pq)){
					return true;
				}
				//next_list.push_back(next);
			}else{
				if(debug)cout<<"State visited previously"<<endl;
			}
		}
		if(s.x+1<k){
			next = transform(s , "down");
			if(state_set.find(next)==state_set.end()){
				if(debug)cout<<"Pushing state to priority queue"<<endl;
				if(push_to_pq(next , pq)){
					return true;
				}
				//next_list.push_back(next);
			}else{
				if(debug)cout<<"State visited previously"<<endl;
			}
		}
		
		/*
		sort(next_list.begin() , next_list.end() , compare());
		for(int i=0;i<next_list.size();++i){
			if(push_to_pq(next_list[i] , pq)){
				return true;
			}
		}*/
		
		return false;
	}
public:
	Solver(int a):
	k(a),
	init_state(State(k)),
	final_state(State(k)),
	pos(vector<pair<int,int> >(k*k)){
		int val=0;
		for(int i=0;i<k;++i){
			for(int j=0;j<k;++j){
				cin>>init_state.grid[i][j];
				if(init_state.grid[i][j] == 0){
					init_state.x = i;
					init_state.y = j;
				}
				pos[val] = make_pair(i,j);
				final_state.grid[i][j] = val++;
			}
		}
		final_state.score = k*k;
		init_state.score  = get_score(init_state , final_state);
	}
	void solve(){
		priority_queue<State, vector<State> , compare> pq;
		//stack<State> pq;
		if(debug){
			cout<<"Pushing initial State "<<endl;
			init_state.print();
		}
		pq.push(init_state);
		state_set.insert(init_state);
		
		State s;
		while(!pq.empty()){
			s = pq.top();
			pq.pop();
			
			if(expand(s , pq)){
				if(debug)cout<<"Final State found"<<endl;
				break;
			}
		}
	}
	void print_path(){
		if(debug){
			cout<<"Final State:"<<endl;
			final_state.print();
		}
		//cout<<path.size()<<endl;
		for(int i=0;i<path.size();++i){
			cout<<path[i]<<endl;
		}
	}
};
int main(int argc , char **argv)
{
	if(argc>1 && strcmp(argv[1],"DEBUG")==0) debug=true;
	int k;
	scanf("%d",&k);
	
	Solver s(k);
	s.solve();
	s.print_path();
	
	return 0;
}
