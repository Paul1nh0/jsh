
function j0(){

    try{}catch(e){}
    //alert('a');

    var a = new Array();
    var b = new Array();
    
    <ffh>

    function opt(a,b){
        <fff>
    }
    
    for (let y = 0; y <= <randint>; ++y)
		opt(a,b);

}

var vars = new Array(102);

var handler0 = {
    get: function(a, b) {
		<fff>
            },
  set: function (a, b) {
		<fff>
  },deleteProperty: function (a, b) {
		<fff>
      },
  enumerate: function (a, b) {
		<fff>
      },
  ownKeys: function (a, b) {
    		<fff>
  },
  has: function (a, b) {
		<fff>
  },
  defineProperty: function (a, b) {
		<fff>
      },
  getOwnPropertyDescriptor: function (a, b) {
		<fff>
         
  },
};
var handler1 = {
    get: function(a, b) {
		<fff>
            },
  set: function (a, b) {
		<fff>
  },deleteProperty: function (a, b) {
		<fff>
      },
  enumerate: function (a, b) {
		<fff>
      },
  ownKeys: function (a, b) {
    		<fff>
  },
  has: function (a, b) {
		<fff>
  },
  defineProperty: function (a, b) {
		<fff>
      },
  getOwnPropertyDescriptor: function (a, b) {
		<fff>
        }, 
};


p0 = new Proxy({}, handler0);
p1 = new Proxy({}, handler1);

var runcount = {main:0, f0:0, f1:0, f2:0, f3:0, f4:0, f5:0, f6:0, f7:0, f8:0, f9:0, p0:0,p1:0}

function main() {
runcount.main++; if(runcount.main>2) return;
//alert('main');
<jsfuzzer>
}

function f0(arg1, arg2, arg3) {
runcount.f0++; if(runcount.f0>2) return;
//alert(0);
<jsfuzzer>
}

function f1(arg4, arg5, arg6) {
runcount.f1++; if(runcount.f1>2) return;
//alert(1);
<jsfuzzer>
}

function f2(arg7, arg8, arg9) {
runcount.f2++; if(runcount.f2>2) return;
//alert(2);
<jsfuzzer>
}

function f3(arg1, arg2, arg3) {
runcount.f3++; if(runcount.f3>2) return;
//alert(3);
<jsfuzzer>
}

function f4(arg4, arg5, arg6) {
runcount.f4++; if(runcount.f4>2) return;
//alert(4);
<jsfuzzer>
}

function f5(arg7, arg8, arg9) {
runcount.f5++; if(runcount.f5>2) return;
//alert(5);
<jsfuzzer>
}

function f6(arg1, arg2, arg3) {
runcount.f6++; if(runcount.f6>2) return;
//alert(6);
<jsfuzzer>
}

function f7(arg4, arg5, arg6) {
runcount.f7++; if(runcount.f7>2) return;
//alert(7);
<jsfuzzer>
}

function f8(arg7, arg8, arg9) {
runcount.f8++; if(runcount.f8>2) return;
//alert(8);
<jsfuzzer>
}

function f9(arg1, arg2, arg3) {
runcount.f9++; if(runcount.f9>2) return;
//alert(9);
<jsfuzzer>
}

for(var i=0;i<20;i++) {
  vars[i] = new Array(10);
}
for(var i=20;i<40;i++) {
  vars[i] = 'aaaaaaaaaa';
}
for(var i=40;i<60;i++) {
  vars[i] = new Array();
}
for(var i=60;i<90;i++) {
  vars[i] = {};
}
vars[90] = f0;
vars[91] = f1;
vars[92] = f2;
vars[93] = f3;
vars[94] = f4;
vars[95] = f5;
vars[96] = f6;
vars[97] = f7;
vars[98] = f8;
vars[99] = f9;
vars[100] = p0;
vars[101] = p1;
vars[75] = j0;

main();


